from pydriller import RepositoryMining
from pydriller.domain.commit import ModificationType
import javalang
import csv
    
def getFirstOfChunkInfo(line):
    infoParts = line.strip().split('@@')
    if len(infoParts) == 3 and line.startswith('@@'): # validate hunk header format
        linesInfo = infoParts[1].split() 
        oldInfo = linesInfo[0].split(',')
        if len(oldInfo) == 1:
            oldInfo.append(0)
        newInfo = linesInfo[1].split(',')
        if len(newInfo) == 1:
            newInfo.append(0)
        linesInfo =  oldInfo + newInfo
        linesInfo[0] = int(linesInfo[0][1:]) - 1
        linesInfo[1] = int(linesInfo[1])
        linesInfo[2] = int(linesInfo[2][1:]) - 1
        linesInfo[3] = int(linesInfo[3])
        return linesInfo # by format: [old first line, old line count, new first line, new line count]
    return None # it is not hunk header

def getOldDocFromDiff(newDoc, diff):
    oldDoc = []
    newDoc = newDoc.split('\n')
    diff = diff.split('\n')
    lineNum = 0
    for index, line in enumerate(diff):
        if line.startswith('\\') or line == '' and index == len(diff) - 1: # sometimes "\ no newlines at the end of file" appears
            continue
        chunkHeader = getFirstOfChunkInfo(line)
        if chunkHeader: # it is chunk header
            oldDoc += newDoc[lineNum : chunkHeader[2]]
            lineNum = chunkHeader[2]
        else: # it is file content
            if line.startswith('-'):
                oldDoc.append(line[1:])
            elif line.startswith('+'):
                lineNum += 1
            else:
                oldDoc.append(newDoc[lineNum])
                lineNum += 1
    oldDoc += newDoc[lineNum:]
    return '\n'.join(oldDoc)

def populateMethod(method, path): # modify method object and add variables that we need
        if path:
            method.name = '::'.join(path) + '::' + method.name
        method.parameters = list(map(lambda parameter: parameter.type.name + '[]' * len(parameter.type.dimensions) + ' ' + parameter.name, method.parameters))
        return_type = ''
        if hasattr(method, 'return_type'): # not constructor
            return_type = 'void '
            if method.return_type: # not void
                return_type = method.return_type.name + '[]' * len(method.return_type.dimensions) + ' '
        modifiers = ' '.join(list(method.modifiers))
        if modifiers:
            modifiers += ' '
        method.signature =  modifiers + return_type + method.name + '(' + ', '.join(method.parameters) + ')'

def parseMethods(code, diff):
    tree = javalang.parse.parse(code) # creates AST from code string
    methods = []
    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        if node.name in diff: # if method doesn't appear in diff string then no parameter is added to it
            populateMethod(node, map(lambda node: node.name, filter(lambda node: hasattr(node, 'name'), path)))
            methods.append(node)
    for path, node in tree.filter(javalang.tree.ConstructorDeclaration):
        if node.name in diff: # if method doesn't appear in diff string then no parameter is added to it
            populateMethod(node, map(lambda node: node.name, filter(lambda node: hasattr(node, 'name'), path)))
            methods.append(node)
    methods.sort(key= lambda item: item.name)
    res = [] # create an array of overloaded methods list
    tmpMethod = None
    for method in methods:
        if tmpMethod and method.name == tmpMethod.name:
            res[-1].append(method)
        else:
            res.append([method])
        tmpMethod = method
    return res # format: [[method1, method2], [method3, method4]]

repo = input('Please type local or remote repository path: ')
outputFilename = input('Please type results filename(without .csv) [default: results]: ')
if not outputFilename:
    outputFilename = 'results'
outfile = open(outputFilename+'.csv', mode='w')
writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerow(['Commit SHA', 'Java File', 'Old function signature', 'New function signature'])
i = 1
for commit in RepositoryMining(repo, only_modifications_with_file_types=['.java']).traverse_commits():
    i += 1
    if i % 100 == 0:
        print(i)
    for modification in commit.modifications:
        if modification.filename.endswith('.java') and modification.change_type != ModificationType.ADD and modification.change_type != ModificationType.DELETE and modification.added > 0 and modification.removed > 0:
            newDoc = modification.source_code
            try:
                newMethods = parseMethods(newDoc, modification.diff)
            except:
                break
            newMethodsNames = set(map(lambda methodlist: methodlist[0].name, newMethods))
            oldDoc = getOldDocFromDiff(newDoc, modification.diff)
            try:
                oldMethods = parseMethods(oldDoc, modification.diff)
            except:
                break
            oldMethodsNames = set(map(lambda methodlist: methodlist[0].name, oldMethods))
            methodNamesIntersection = oldMethodsNames & newMethodsNames # remove functions which are not in both files
            for oldMethodlist in oldMethods:
                if oldMethodlist[0].name not in methodNamesIntersection:
                    continue
                for newMethodlist in newMethods:
                    if newMethodlist[0].name != oldMethodlist[0].name:
                        continue
                    for newMethod in newMethodlist:
                        maxNum = 0
                        counterOldMethod = None
                        newParamsSet = set(newMethod.parameters)
                        for oldMethod in oldMethodlist:
                            intersection = len(newParamsSet & set(oldMethod.parameters))
                            if len(newParamsSet) > intersection and len(oldMethod.parameters) == intersection and len(oldMethod.parameters) > maxNum:
                                maxNum = len(oldMethod.parameters)
                                counterOldMethod = oldMethod
                        if counterOldMethod: # added parameter detected
                            writer.writerow([commit.hash, modification.new_path, counterOldMethod.signature, newMethod.signature])
                    break
print('Repository has been successfully mined!')
print('You can see the results in ' + outputFilename + '.csv')
outfile.close()