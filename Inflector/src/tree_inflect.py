#!/usr/bin/env python

'''                   yatbear
               sapphirejyt@gmail.com

                  HW 5 - Inflector
      unigram LM incorporating dependency trees
            JHU 600.468 Machine Translation         '''

import argparse
import codecs
import sys
import os
from collections import defaultdict
from itertools import izip
from tree import DepTree

parser = argparse.ArgumentParser(description="Inflect a lemmatized corpus")
parser.add_argument("-t", type=str, default="data/train", help="training data prefix")
parser.add_argument("-d", type=str, default="data/dtest", help="test data prefix")
parser.add_argument("-l", type=str, default="lemma", help="lemma file suffix")
parser.add_argument("-w", type=str, default="form", help="word file suffix")
parser.add_argument("-r", type=str, default="tree", help="dependency tree suffix")
args = parser.parse_args()

# Python sucks at UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

def inflections(word, lemma, tree):
    if LEMMAS.has_key((lemma, tree)):
        return sorted(LEMMAS[(lemma, tree)].keys(), lambda x, y: cmp(LEMMAS[(lemma, tree)][y], LEMMAS[(lemma, tree)][x]))
    elif LEMMAS.has_key(lemma):
        return sorted(LEMMAS[lemma].keys(), lambda x, y: cmp(LEMMAS[lemma][y], LEMMAS[lemma][x]))
    return [lemma]

def best_inflection(word, lemma, tree):
    return inflections(word, lemma, tree)[0]

if __name__ == '__main__':
    # Build a simple unigram model on the training data
    LEMMAS = defaultdict(defaultdict)
    if args.t:
        def combine(a, b): return '%s.%s' % (a, b)
        def utf8read(file): return codecs.open(file, 'r', 'utf-8')
        # Build the LEMMAS hash, a two-level dictionary mapping lemmas to inflections to counts
        train_words = utf8read(combine(args.t, args.w))
        train_lemmas = utf8read(combine(args.t, args.l))
        train_trees = utf8read(combine(args.t, args.r))
        for words, lemmas, treestr in izip(train_words, train_lemmas, train_trees):
            w = words.rstrip().lower().split()
            l = lemmas.rstrip().lower().split()
            t = DepTree(treestr)
            for word, lemma, node in izip(w, l, t):
                tree = (node.parent_index(), node.label())
                LEMMAS[lemma][word] = LEMMAS[lemma].get(word, 0) + 1
                LEMMAS[(lemma, tree)][word] = LEMMAS[(lemma, tree)].get(word, 0) + 1

    # Choose the most common inflection for each word and output them as a sentence
    test_words = utf8read(combine(args.d, args.w))
    test_lemmas = utf8read(combine(args.d, args.l))
    test_trees = utf8read(combine(args.d, args.r))
    for words, lemmas, treestr in izip(test_words, test_lemmas, test_trees):
        w = words.rstrip().lower().split()
        l = lemmas.rstrip().lower().split()
        t = DepTree(treestr)
        print ' '.join([best_inflection(x, y, (z.parent_index(), z.label())) for x, y, z in izip(w, l, t)])
