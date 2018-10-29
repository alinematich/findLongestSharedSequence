import math
import re

file1 = []
with open('mineRepoCommits.py') as file:
    file1 = re.sub(r'([\n]|\s)+', ' ', file.read()).split()

file2 = []
with open('findSequences.py') as file:
    file2 =  re.sub(r'([\n]|\s)+', ' ', file.read()).split()

codes = [file1, file2]
tokenSequences = set()
for code in codes:
    for length in range(2, len(code)+1):
        for index in range(0, len(code) - length + 1):
            tokenSequences.add(tuple(code[index:index+length]))

scores = {}
for index, seq in enumerate(tokenSequences):
    score = 0
    seqlist = list(seq)
    if (index+1) % 10000 == 0:
        print(index+1, '/', len(tokenSequences))
    for code in codes:
        for index in range(0, len(code) - len(seq) + 1):
            if seqlist == code[index:index+len(seqlist)]:
                scores[seq] = scores.get(seq, 0) + 1
                break

scores = [((math.log2(len(k)) * math.log2(v)) , k) for k, v in scores.items() if v > 1]
scores.sort(key=lambda item: item[0], reverse= True)
for i in scores[:20]:
    print(i)
    print()
    print('------------------------------#####')