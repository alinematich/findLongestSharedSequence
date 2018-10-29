import math
from os import listdir
from os.path import isfile, isdir, join
import javalang
import csv
import sys

tokenize = lambda string: list(map(lambda token: token.value, javalang.tokenizer.tokenize(string+'\n')))

def longestCommonSequences(codes):
    scores = {}
    for i, code in enumerate(codes):
        print(i, filenames[i], len(code))
        for length in range(2, min([500, len(code)+1])):
            for index in range(0, len(code) - length + 1):
                tpl = hash(tuple(code[index:index+length]))
                scores[tpl] = scores.get(tpl, 0) + 1
            if length % 100 == 0:
                print(length)
    scores = {k: v for k, v in scores.items() if v > 1}
    # scores.sort(key=lambda item: item[0], reverse= True)
    # scores = [{'score': (math.log2(len(k)) * math.log2(v)),'count': v ,'seq': k} for k, v in scores.items() if v > 1]
    # scores.sort(key=lambda item: item['score'], reverse= True)
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

# with open(sys.argv[2], mode='w') as outfile:
#     writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     writer.writerow(['Score', 'Tokens', 'Count', 'Source Code'])
#     writer.writerows(list(map(lambda item: [item['score'], len(item['seq']), item['count'], list(item['seq'])], longestCommonSequences(codes))))

def saveToCsv(hashedResult):
    seen = set()
    f = open(sys.argv[2], mode='w')
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Score', 'Tokens', 'Count', 'Source Code'])
    finished = False
    for i, code in enumerate(codes):
        print(i, filenames[i], len(code))
        for length in range(2, min([500, len(code)+1])):
            for index in range(0, len(code) - length + 1):
                tp = code[index:index+length]
                hs = hash(tuple(tp))
                if hs not in seen and hs in hashedResult:
                    seen.add(hs)
                    val = hashedResult[hs]
                    writer.writerow([(math.log2(len(tp)) * math.log2(val)), len(tp), val, tp])
                    if len(seen) == len(hashedResult):
                        finished = True
                        break
            if length % 100 == 0:
                print(length)
            if finished:
                break
        if finished:
            break
    f.close()

saveToCsv(longestCommonSequences(codes))