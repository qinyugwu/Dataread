# -*- coding: utf-8 -*-
#!/usr/bin/python
from __future__ import print_function
import sys
from os import walk
import os
import re
import string
import pprint
from nltk.corpus import stopwords
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

parser = spacy.load('en')

def listFiles(mypath):
    """get all files in the path"""
    files = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        files.extend(filenames)
    return files

def getStringItems(stringlist):
    """get strings from list data"""
    items = []
    if type(stringlist) is str:    
        for strings in data:
            if (key == 'lineItems'):
                items.extend(data[key])
            # elif (key == 'pageType'):
    elif type(data) is list:
        for d in data:
            items.extend(getLineItems(d))
    return items

def remove_punctuation(text):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    s = regex.sub(' ', text)
    return s

def remove_formatting(text):
    output = text.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ').replace('\x0b', ' ').replace('\x0c', ' ')
    return output

def transform_for_classifier(text):
    temp = remove_punctuation(text)
    final = remove_formatting(temp)
    return final

STOPLIST = set(stopwords.words('english') + ['n\'t', '\'s', '\'m', 'ca'] + list(ENGLISH_STOP_WORDS))
SYMBOLS = ' '.join(string.punctuation).split(' ') + ['-----', '---', '...', '"', '"', '\'ve']

def removeStrings(string, removeList):
    strList = string.split(' ')
    newList = []
    for item in strList:
        if not item in removeList:
            newList.append(item)
    newString = ' '.join(newList)
    return newString

def tokenizeText(sample):
    tokens = parser(sample)
    lemmas = []
    for tok in tokens:
        lemmas.append(tok.lemma_.lower().strip())
    tokens = [tok for tok in tokens if tok not in STOPLIST]
    tokens = [tok for tok in tokens if tok not in SYMBOLS]
    while "" in tokens:
        tokens.remove("")
    while " " in tokens:
        tokens.remove(" ")
    while "\n" in tokens:
        tokens.remove("\n")
    while "\n\n" in tokens:
        tokens.remove("\n\n")
    tokenStrings = [str(tok) for tok in tokens]
    for strings in tokenStrings:
        strings.replace(' ', '')
    newText = ' '.join(tokenStrings)
    return newText

def cleanUpText(inputText, filterList):
    noFilters = removeStrings(inputText, filterList)
    tokenized = tokenizeText(noFilters)
    return tokenized

def main(path):
    """print all the results for demo"""
    for item in cleanUpText(path):
        pprint.pprint(item)

if __name__ == "__main__":
    main(sys.argv[1])
