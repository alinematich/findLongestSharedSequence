import math
import re
from os import listdir
from os.path import isfile, isdir, join
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, ' '.join(a), ' '.join(b)).ratio() > 0.8

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
for i, score in enumerate(scores):
    if i % 50 == 0:
        print(i)
    scoreExists = False
    for res in results:
        if similar(res[1], score[1]):
            scoreExists = True
            break
    if not scoreExists:
        results.append(score)
    if len(results) == 20:
        break

for i in results:
    print(i)
    print()
    print('------------------------------#####')