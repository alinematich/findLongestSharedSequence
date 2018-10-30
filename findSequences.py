import math
from os import listdir
from os.path import isfile, isdir, join
import javalang
import csv
import sys

tokenize = lambda string: list(map(lambda token: token.value, javalang.tokenizer.tokenize(string+'\n')))

def longestCommonSequencesLimited(codes, scores, minLength, maxLength, ignoredfiles):
    scores={}
    for i, code in enumerate(codes):
        if len(code) < minLength or i in ignoredfiles:
            continue
        print(i, filenames[i], len(code), minLength, maxLength)
        for length in range(max([2, minLength]), min([maxLength+1, len(code)+1])):
            for index in range(0, len(code) - length + 1):
                tpl = ' '.join(code[index:index+length])
                score = scores.get(tpl, (0, frozenset()))
                scores[tpl] = (score[0] + 1, score[1] | frozenset([i]))
    scores = {k: v for k, v in scores.items() if v[0] > 1}
    filesUsed = set()
    for score, tup in scores.items():
        for fileUsed in tup[1]:
            filesUsed.add(fileUsed)
    for i in set(range(len(codes)))-filesUsed:
        ignoredfiles.add(i)
    return scores

def longestCommonSequences(codes):
    block = 100
    scores = []
    ignored = set()
    for i in range(block, len(max(codes, key=lambda code: len(code)))+block, block):
        scores += [longestCommonSequencesLimited(codes, scores, i - block, i, ignored)]
        if len(max(scores[-1].keys(), key=lambda item: len(item.split())).split()) < i:
            break
    res = []
    for score in scores:
        res += [{'score': (math.log2(len(k.split())) * math.log2(v[0])),'count': v[0] ,'seq': k.split()} for k, v in score.items() if v[0] > 1]
    res.sort(key=lambda item: item['score'], reverse= True)
    return res

def getAllFiles(path, ext):
    files = []
    for f in listdir(path):
        fn = join(path, f)
        if isfile(fn) and fn.endswith('.'+ext):
            files.append(fn)
        elif isdir(fn):
            files += getAllFiles(fn, ext)
    return files

filenames = getAllFiles(sys.argv[1], 'java')
codes = []
for filename in filenames:
    with open(filename) as infile:
        codes += [tokenize(infile.read())]

with open(sys.argv[2], mode='w') as outfile:
    writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Score', 'Tokens', 'Count', 'Source Code'])
    writer.writerows(list(map(lambda item: [item['score'], len(item['seq']), item['count'], list(item['seq'])], longestCommonSequences(codes))))