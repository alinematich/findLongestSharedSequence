# findLongestSharedSequence
Takes a directory address and a filename, then checks all Java files in the directory recursively to find duplicate code.

## Installation
Install python3
```sh
$ sudo apt-get update
$ sudo apt-get install python3.6
```

Install javalang

```sh
$ pip install javalang
```
javalang package: https://github.com/c2nes/javalang

## Usage

```sh
$ python3 findSequences.py ../repos/Java/ res.csv
```

## Tests

This code is already ran on these two files:

Directory: https://github.com/iluwatar/java-design-patterns/tree/master/abstract-document

Result: https://github.com/alinematich/findLongestSharedSequence/blob/master/results/abstract-document-Results.csv

Directory: https://github.com/TheAlgorithms/Java

Result: The size of the result file was almost 800MB so I did not upload it.
