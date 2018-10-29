import math
import re
from os import listdir
from os.path import isfile, isdir, join

def getAllFiles(path, ext):
    files = []
    for f in listdir(path):
        fn = join(path, f)
        if isfile(fn) and fn.endswith('.'+ext):
            files.append(fn)
        elif isdir(fn):
            files += getAllFiles(fn, ext)
    return files
filenames = getAllFiles('../repos/java-design-patterns/abstract-document/src/', 'java')
# filenames = ['mineRepoCommits.py', 'findSequences.py']

codes = []
for filename in filenames:
    with open(filename) as infile:
        codes += [re.sub(r'([\n]|\s)+', ' ', infile.read()).split()]

scores = {}
for code in codes:
    for length in range(2, len(code)+1):
        for index in range(0, len(code) - length + 1):
            tpl = tuple(code[index:index+length])
            scores[tpl] = scores.get(tpl, 0) + 1

scores = [((math.log2(len(k)) * math.log2(v)) , k) for k, v in scores.items() if v > 1]
scores.sort(key=lambda item: item[0], reverse= True)
results = []
for score in scores:
    scoreExists = False
    for res in results:
        for i in range(len(res[1])-len(score[1])+1):
            if score[1] == res[1][i:i+len(score[1])]:
                scoreExists = True
                break
        if scoreExists:
            break
        for i in range(len(score[1])-len(res[1])+1):
            if res[1] == score[1][i:i+len(res[1])]:
                scoreExists = True
                break
        if scoreExists:
            break
    if not scoreExists:
        results.append(score)
    if len(results) == 20:
        break

for i in results:
    print(i)
    print()
    print('------------------------------#####')