#!/usr/bin/env python

import nltk,sys

while True:
    line = sys.stdin.readline().rstrip('\n')
    tokens = nltk.word_tokenize(line)
    print tokens
    #tagged = nltk.pos_tag(tokens)
    #tagged[0:6]
