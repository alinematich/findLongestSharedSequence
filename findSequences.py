import math
from os import listdir
from os.path import isfile, isdir, join
import javalang

tokenize = lambda string: list(map(lambda token: token.value, javalang.tokenizer.tokenize(string+'\n')))

def longestCommonSequences(codes):
    scores = {}
    for code in codes:
        for length in range(2, len(code)+1):
            for index in range(0, len(code) - length + 1):
                tpl = tuple(code[index:index+length])
                scores[tpl] = scores.get(tpl, 0) + 1

    scores = [{'score': (math.log2(len(k)) * math.log2(v)),'count': v ,'seq': k} for k, v in scores.items() if v > 1]
    scores.sort(key=lambda item: item['score'], reverse= True)
    return scores

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
codes = []
for filename in filenames:
    with open(filename) as infile:
        codes += [tokenize(infile.read())]

print(longestCommonSequences(codes))