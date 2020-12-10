########################################
## CS447 Natural Language Processing  ##
##           Homework 3               ##
##       Yifan Shi                    ##
##       yifans16@illnois.edu         ##
########################################
##
## Part 1:
## Train a bigram HMM for POS tagging
##
import os.path
import sys
from operator import itemgetter
from collections import defaultdict
from math import log

# Unknown word token
UNK = 'UNK'

# Class that stores a word and tag together
class TaggedWord:
    def __init__(self, taggedString):
        parts = taggedString.split('_')
        self.word = parts[0]
        self.tag = parts[1]

class node:
    def __init__(self, val = float('-inf'), idx = -1):
        self.val = val
        self.idx = idx

# Class definition for a bigram HMM
class HMM:
### Helper file I/O methods ###
    ################################
    #intput:                       #
    #    inputFile: string         #
    #output: list                  #
    ################################
    # Reads a labeled data inputFile, and returns a nested list of sentences, where each sentence is a list of TaggedWord objects
    def readLabeledData(self, inputFile):
        if os.path.isfile(inputFile):
            file = open(inputFile, "r") # open the input file in read-only mode
            sens = []
            for line in file:
                raw = line.split()
                sentence = []
                for token in raw:
                    sentence.append(TaggedWord(token))
                sens.append(sentence) # append this list as an element to the list of sentences
            return sens
        else:
            print("Error: labeled data file %s does not exist" % inputFile)  # We should really be throwing an exception here, but for simplicity's sake, this will suffice.
            sys.exit() # exit the script

    ################################
    #intput:                       #
    #    inputFile: string         #
    #output: list                  #
    ################################
    # Reads an unlabeled data inputFile, and returns a nested list of sentences, where each sentence is a list of strings
    def readUnlabeledData(self, inputFile):
        if os.path.isfile(inputFile):
            file = open(inputFile, "r") # open the input file in read-only mode
            sens = []
            for line in file:
                sentence = line.split() # split the line into a list of words
                sens.append(sentence) # append this list as an element to the list of sentences
            return sens
        else:
            print("Error: unlabeled data file %s does not exist" % inputFile)  # We should really be throwing an exception here, but for simplicity's sake, this will suffice.
            sys.exit() # exit the script
### End file I/O methods ###

    ################################
    #intput:                       #
    #    unknownWordThreshold: int #
    #output: None                  #
    ################################
    # Constructor
    def __init__(self, unknownWordThreshold=5):
        # Unknown word threshold, default value is 5 (words occuring fewer than 5 times should be treated as UNK)
        self.minFreq = unknownWordThreshold
        ### Initialize the rest of your data structures here ###

        self.tempCount= {}
        self.tagCount = {}
        self.wordCount = {}
        self.wntCount = {} # word and tag
        self.tagCount2 = {} # curr and prev tag
        self.tagVocab = {}
        self.tagTotal = 0.0

    ################################
    #intput:                       #
    #    trainFile: string         #
    #output: None                  #
    ################################
    # Given labeled corpus in trainFile, build the HMM distributions from the observed counts
    def train(self, trainFile):
        data = self.readLabeledData(trainFile) # data is a nested list of TaggedWords
        #print("Your first task is to train a bigram HMM tagger from an input file of POS-tagged text")

        for d in data:
            for temp in d:
                self.tempCount[temp.word] = self.tempCount.get(temp.word, 0) + 1
        
        for d in data:
            for i in range(len(d)):
                w = self.tempCount[d[i].word]
                if w < self.minFreq:
                    d[i].word = UNK

        for d in data:
            prev= TaggedWord("@_@")
            for temp in d:
                self.tagCount[temp.tag] = self.tagCount.get(temp.tag, 0.0) + 1.0
                self.wordCount[temp.word] = self.wordCount.get(temp.word, 0.0) + 1.0
                self.wntCount[temp.word + "_" + temp.tag] = self.wntCount.get(temp.word + "_" + temp.tag, 0.0) + 1.0
                self.tagTotal += 1.0
                if prev.tag == "@":
                    prev = temp
                    continue
                self.tagCount2[temp.tag + "_" + prev.tag] = self.tagCount2.get(temp.tag + "_" + prev.tag, 0.0) + 1.0
                prev = temp

        for key in list(self.tagCount.keys()):
            for k in list(self.tagCount2.keys()):
                if k.find("_" + key) == -1:
                    continue
                self.tagVocab[key] = self.tagVocab.get(key, 0.0) + 1.0

    ################################
    #intput:                       #
    #     testFile: string         #
    #    outFile: string           #
    #output: None                  #
    ################################
    # Given an unlabeled corpus in testFile, output the Viterbi tag sequences as a labeled corpus in outFile
    def test(self, testFile, outFile):
        data = self.readUnlabeledData(testFile)
        for d in data:
            for i in range(len(d)):
                w = self.tempCount.get(d[i], 0)
                if w < self.minFreq:
                    d[i] = UNK
        f=open(outFile, 'w+')
        for sen in data:
            vitTags = self.viterbi(sen)
            senString = ''
            for i in range(len(sen)):
                senString += sen[i]+"_"+vitTags[i]+" "
            print(senString.rstrip(), end="\n", file=f)

    ################################
    #intput:                       #
    #    words: list               #
    #output: list                  #
    ################################
    # Given a list of words, runs the Viterbi algorithm and returns a list containing the sequence of tags
    # that generates the word sequence with highest probability, according to this HMM
    def viterbi(self, words):
        #print("Your second task is to implement the Viterbi algorithm for the HMM tagger")
        # returns the list of Viterbi POS tags (strings)
        wordNum, tagNum = len(words), len(self.tagCount)
        tag = list(self.tagCount.keys())
        trellis = [[node() for _ in range(tagNum)] for _ in range(wordNum)]

        for w in range(wordNum):
            curr = UNK
            if words[w] in list(self.wordCount.keys()):
                curr = words[w]

            for t in range(tagNum):
                neg = (self.wntCount.get(curr + "_" + tag[t], 0.0)) / (self.tagCount[tag[t]])
                if neg == 0:
                    neg = float('-inf')
                else:
                    neg = log(neg)
                if w == 0:
                    trellis[w][t].val = log((self.tagCount[tag[t]] + 1.0) / (self.tagTotal + tagNum)) + neg
                    continue

                valMax, idxMax = float('-inf'), 0
                if words[w] == "," and tag[t] ==",":
                    trellis[w][t].val = 0.0
                for i in range(tagNum):
                    if words[w] == "," and tag[t] != ",":
                        temp = float('-inf')
                    else:
                        temp = trellis[w - 1][i].val + log((self.tagCount2.get(tag[t] + "_" + tag[i], 0.0) + 1.0) / (self.tagCount[tag[i]] + self.tagVocab[tag[i]]))

                    if temp > valMax:
                        valMax, idxMax = temp, i
                if words[w] != ",":
                    trellis[w][t].val = valMax + neg
                trellis[w][t].idx = idxMax
        
        wordMax, tagMax = float('-inf'), 0
        out = []
        for t in range(tagNum):
            if trellis[wordNum - 1][t].val > wordMax:
                wordMax, tagMax = trellis[wordNum - 1][t].val, t

        idx = tagMax
        for w in range(wordNum - 1, 0, -1):
            out.insert(0, tag[idx])
            idx = trellis[w][idx].idx
        out.insert(0, tag[idx])

        return out

if __name__ == "__main__":
    tagger = HMM()
    tagger.train('train.txt')
    tagger.test('test.txt', 'out.txt')
