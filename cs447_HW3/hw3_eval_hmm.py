########################################
## CS447 Natural Language Processing  ##
##           Homework 3               ##
##       Yifan Shi                    ##
##       yifans16@illnois.edu         ##
########################################
##
## Part 1:
## Evaluate the output of your bigram HMM POS tagger
##
import os.path
import sys
from operator import itemgetter

# Unknown word token
UNK = 'UNK'

# Class that stores a word and tag together
class TaggedWord:
    def __init__(self, taggedString):
        parts = taggedString.split('_')
        self.word = parts[0]
        self.tag = parts[1]

# A class for evaluating POS-tagged data
class Eval:
    ################################
    #intput:                       #
    #    goldFile: string          #
    #    testFile: string          #
    #output: None                  #
    ################################
    def __init__(self, goldFile, testFile):
        #print("Your task is to implement an evaluation program for POS tagging")
        self.wordTrue = 0.0
        self.wordTotal = 0.0
        self.senTrue = 0.0
        self.senTotal = 0.0
        self.tagCount = {}
        self.TP = {}
        self.FP = {}
        self.FN = {}

        if os.path.isfile(goldFile):
            gF = open(goldFile, "r")
            gSen = []
            for g in gF:
                raw = g.split()
                temp = []
                for token in raw:
                    temp.append(TaggedWord(token))
                    self.tagCount[TaggedWord(token).tag] = self.tagCount.get(TaggedWord(token).tag, 0.0) + 1.0
                gSen.append(temp)

        if os.path.isfile(testFile):
            tF = open(testFile, "r")
            tSen = []
            for t in tF:
                raw = t.split()
                temp = []
                for token in raw:
                    temp.append(TaggedWord(token))
                tSen.append(temp)

        temp = list(self.tagCount.keys())
        self.confusion = [[0 for _ in range(len(temp))] for _ in range(len(temp))]
        for i in range(len(gSen)):
            wrong = 0
            self.senTotal += 1.0
            for j in range(len(gSen[i])):
                self.wordTotal += 1.0
                gWord, tWord = gSen[i][j], tSen[i][j]
                self.confusion[temp.index(gWord.tag)][temp.index(tWord.tag)] += 1
                if gWord.tag == tWord.tag:         
                    self.wordTrue += 1.0
                    self.TP[gWord.tag] = self.TP.get(gWord.tag, 0.0) + 1.0
                else:
                    wrong += 1
                    self.FP[tWord.tag] = self.FP.get(tWord.tag, 0.0) + 1.0
                    self.FN[gWord.tag] = self.FN.get(gWord.tag, 0.0) + 1.0
            if wrong == 0:
                self.senTrue += 1.0
                




    ################################
    #intput: None                  #
    #output: float                 #
    ################################
    def getTokenAccuracy(self):
        #print("Return the percentage of correctly-labeled tokens")
        return self.wordTrue / self.wordTotal

    ################################
    #intput: None                  #
    #output: float                 #
    ################################
    def getSentenceAccuracy(self):
        #print("Return the percentage of sentences where every word is correctly labeled")
        return self.senTrue / self.senTotal

    ################################
    #intput:                       #
    #    outFile: string           #
    #output: None                  #
    ################################
    def writeConfusionMatrix(self, outFile):
        #print("Write a confusion matrix to outFile; elements in the matrix can be frequencies (you don't need to normalize)")
        f=open(outFile, 'w+')
        temp = list(self.tagCount.keys())
        row1 = "\t"
        for i in range(len(temp)):
            row1 += temp[i] + '\t'
        print(row1.rstrip(), end="\n", file = f)

        for i in range(len(temp)):
            row = ""
            row += temp[i] + '\t'
            for j in range(len(temp)):
                row += str(self.confusion[i][j]) + '\t'
            print(row.rstrip(), end="\n", file=f)

    ################################
    #intput:                       #
    #    tagTi: string             #
    #output: float                 #
    ################################
    def getPrecision(self, tagTi):
        #print("Return the tagger's precision when predicting tag t_i")
        if tagTi in self.TP:
            return self.TP[tagTi] / (self.TP[tagTi] + self.FP.get(tagTi, 0.0))
        return 0.0

    ################################
    #intput:                       #
    #    tagTi: string             #
    #output: float                 #
    ################################
    # Return the tagger's recall on gold tag t_j
    def getRecall(self, tagTj):
        #print("Return the tagger's recall for correctly predicting gold tag t_j")
        if tagTj in self.TP:
            return self.TP[tagTj] / (self.TP[tagTj] + self.FN.get(tagTj, 0.0))
        return 0.0


if __name__ == "__main__":
    # Pass in the gold and test POS-tagged data as arguments
    if len(sys.argv) < 2:
        print("Call hw2_eval_hmm.py with two arguments: gold.txt and out.txt")
    else:
        gold = sys.argv[1]
        test = sys.argv[2]
        # You need to implement the evaluation class
        eval = Eval(gold, test)
        # Calculate accuracy (sentence and token level)
        print("Token accuracy: ", eval.getTokenAccuracy())
        print("Sentence accuracy: ", eval.getSentenceAccuracy())
        # Calculate recall and precision
        print("Recall on tag NNP: ", eval.getRecall('NNP'))
        print("Precision for tag NNP: ", eval.getPrecision('NNP'))
        # Write a confusion matrix
        eval.writeConfusionMatrix("confusion_matrix.txt")
