import math
from os import listdir
from os.path import isfile, isdir, join
import javalang
import csv
import sys

tokenize = lambda string: list(map(lambda token: token.value, javalang.tokenizer.tokenize(string+'\n')))

def longestCommonSequencesLimited(codes, scores, minLength, maxLength):
    for i, code in enumerate(codes):
        if len(code) < minLength:
            continue
        print(i, filenames[i], len(code), minLength, maxLength)
        for length in range(max([2, minLength]), min([maxLength, len(code)+1])):
            for index in range(0, len(code) - length + 1):
                tpl = ' '.join(code[index:index+length])
                scores[tpl] = scores.get(tpl, 0) + 1
            if length % 100 == 0:
                print(length)
    scores = {k: v for k, v in scores.items() if v > 1}
    return scores

def longestCommonSequences(codes):
    block = 100
    scores = {}
    for i in range(block, max(list(map(lambda code: len(code), codes)))+block, block):
        scores = longestCommonSequencesLimited(codes, scores, i - block, i + 1)
        print(max(list(map(lambda item: len(item.split()), scores.keys()))))
        if max(list(map(lambda item: len(item.split()), scores.keys()))) < i:
            break
    scores = [{'score': (math.log2(len(k.split())) * math.log2(v)),'count': v ,'seq': k.split()} for k, v in scores.items() if v > 1]
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

filenames = getAllFiles(sys.argv[1], 'java')
codes = []
for filename in filenames:
    with open(filename) as infile:
        codes += [tokenize(infile.read())]

with open(sys.argv[2], mode='w') as outfile:
    writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Score', 'Tokens', 'Count', 'Source Code'])
    writer.writerows(list(map(lambda item: [item['score'], len(item['seq']), item['count'], list(item['seq'])], longestCommonSequences(codes))))