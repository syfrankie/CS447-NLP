########################################
## CS447 Natural Language Processing  ##
##           Homework 1               ##
##       Julia Hockenmaier            ##
##       juliahmr@illnois.edu         ##
########################################
##
## Part 1:
## Develop a smoothed n-gram language model and evaluate it on a corpus
##
import os.path
import sys
import random
import math
from operator import itemgetter
from collections import defaultdict
#----------------------------------------
#  Data input 
#----------------------------------------

# Read a text file into a corpus (list of sentences (which in turn are lists of words))
# (taken from nested section of HW0)
def readFileToCorpus(f):
    """ Reads in the text file f which contains one sentence per line.
    """
    if os.path.isfile(f):
        file = open(f, "r") # open the input file in read-only mode
        i = 0 # this is just a counter to keep track of the sentence numbers
        corpus = [] # this will become a list of sentences
        print("Reading file ", f)
        for line in file:
            i += 1
            sentence = line.split() # split the line into a list of words
            #append this lis as an element to the list of sentences
            corpus.append(sentence)
            if i % 1000 == 0:
    	#print a status message: str(i) turns int i into a string
    	#so we can concatenate it
                sys.stderr.write("Reading sentence " + str(i) + "\n")
        #endif
    #endfor
        return corpus
    else:
    #ideally we would throw an exception here, but this will suffice
        print("Error: corpus file ", f, " does not exist")
        sys.exit() # exit the script
    #endif
#enddef


# Preprocess the corpus to help avoid sess the corpus to help avoid sparsity
def preprocess(corpus):
    #find all the rare words
    freqDict = defaultdict(int)
    for sen in corpus:
	    for word in sen:
	       freqDict[word] += 1
	#endfor
    #endfor

    #replace rare words with unk
    for sen in corpus:
        for i in range(0, len(sen)):
            word = sen[i]
            if freqDict[word] < 2:
                sen[i] = UNK
	    #endif
	#endfor
    #endfor

    #bookend the sentences with start and end tokens
    for sen in corpus:
        sen.insert(0, start)
        sen.append(end)
    #endfor
    
    return corpus
#enddef

def preprocessTest(vocab, corpus):
    #replace test words that were unseen in the training with unk
    for sen in corpus:
        for i in range(0, len(sen)):
            word = sen[i]
            if word not in vocab:
                sen[i] = UNK
	    #endif
	#endfor
    #endfor
    
    #bookend the sentences with start and end tokens
    for sen in corpus:
        sen.insert(0, start)
        sen.append(end)
    #endfor

    return corpus
#enddef

# Constants 
UNK = "UNK"     # Unknown word token
start = "<s>"   # Start-of-sentence token
end = "</s>"    # End-of-sentence-token


#--------------------------------------------------------------
# Language models and data structures
#--------------------------------------------------------------

# Parent class for the three language models you need to implement
class LanguageModel:
    # Initialize and train the model (ie, estimate the model's underlying probability
    # distribution from the training corpus)
    def __init__(self, corpus):
        """Your task is to implement five kinds of n-gram language models:
        a) an (unsmoothed) unigram model (UnigramModel)
        b) a unigram model smoothed using Laplace smoothing (SmoothedUnigramModel)
        c) an unsmoothed bigram model (BigramModel)
        """
        self.total = 0
        self.unidict = {}
        self.bidict = {}
        self.count = 0

        # unicount
        #count = 0
        for sen in corpus:
            for w in sen:
                if w != start:
                    self.total += 1
                    self.unidict[w] = self.unidict.get(w, 0) + 1
                else:
                    self.count += 1
        #self.unidict[start] = count

        # bicount
        prev = start
        for sen in corpus:
            for w in sen:
                if w != start:
                    temp = w + " " + prev
                    self.bidict[temp] = self.bidict.get(temp, 0) + 1
                prev = w

    #enddef

    # Generate a sentence by drawing words according to the 
    # model's probability distribution
    # Note: think about how to set the length of the sentence 
    #in a principled way
    def generateSentence(self):
        # Implement the generateSentence method in each subclass
        return " "
    #emddef

    # Given a sentence (sen), return the probability of 
    # that sentence under the model
    def getSentenceProbability(self, sen):
        # Implement the getSentenceProbability method in each subclass
        return 0.0
    #enddef

    # Given a corpus, calculate and return its perplexity 
    #(normalized inverse log probability)
    def getCorpusPerplexity(self, corpus):
        return 0.0
    #enddef

    # Given a file (filename) and the number of sentences, generate a list
    # of sentences and write each to file along with its model probability.
    # Note: you shouldn't need to change this method
    def generateSentencesToFile(self, numberOfSentences, filename):
        filePointer = open(filename, 'w+')
        for i in range(0,numberOfSentences):
            sen = self.generateSentence()
            prob = self.getSentenceProbability(sen)
            stringGenerated = str(prob) + " " + " ".join(sen) 
            
	    #endfor
    #enddef
#endclass

# Unigram language model
class UnigramModel(LanguageModel):
    def generateSentence(self):
        out = [start]
        curr = start
        while curr != end:
            temp = random.random()
            for w in self.unidict.keys():
                temp -= self.unidict[w] / self.total
                if temp <= 0:
                    break
            curr = w
            out.append(curr)
        return out
    #enddef

    def getSentenceProbability(self, sen):
        p = 0.0
        for w in sen:
            if w != start:
                temp = self.unidict.get(w, 0)
                if temp == 0:
                    return 0
                p += math.log(temp / self.total)
        return math.exp(p)
    #enddef

    
    def getCorpusPerplexity(self, corpus):
        p = 0.0
        count = 0
        for s in corpus:
            for w in s:
                if w != start:
                    count += 1
                    p += math.log(self.unidict[w] / self.total)
        return math.exp(-1 / count * p)
    #enddef
    
#endclass

#Smoothed unigram language model (use laplace for smoothing)
class SmoothedUnigramModel(LanguageModel):
    def generateSentence(self):
        out = [start]
        curr = start
        while curr != end:
            temp = random.random()
            for w in self.unidict.keys():
                temp -= (self.unidict[w] + 1) / (self.total + len(self.unidict.keys()))
                if temp <= 0:
                    break
            curr = w
            out.append(curr)
        return out
    #enddef

    def getSentenceProbability(self, sen):
        p = 0.0
        for w in sen:
            if w != start:
                p += math.log((self.unidict[w] + 1) / (self.total + len(self.unidict.keys())))
        return math.exp(p)
    #endddef

    
    def getCorpusPerplexity(self, corpus):
        p = 0.0
        count = 0
        for s in corpus:
            for w in s:
                if w != start:
                    count += 1
                    p += math.log((self.unidict[w] + 1) / (self.total + len(self.unidict.keys())))
        return math.exp(-1 / count * p)
    #enddef
#endclass

# Unsmoothed bigram language model
class BigramModel(LanguageModel):
    def generateSentence(self):
        out = [start]
        curr = start
        while curr != end:
            temp = random.random()
            for w in self.unidict.keys():
                if curr == start:
                    num = self.count
                else:
                    num = self.unidict[curr]
                temp -= self.bidict.get(w + " " + curr, 0) / num
                if temp <= 0:
                    break
            curr = w
            out.append(curr)
        return out
    #enddef

    def getSentenceProbability(self, sen):
        p = 0.0
        prev = "#"
        for w in sen:
            if w == start:
                prev = w
                continue
            if self.bidict.get(w + " " + prev, 0) == 0:
                return 0.0
            if prev == start:
                num = self.count
            else:
                num = self.unidict[prev]
            p += math.log(self.bidict[w + " " + prev] / num)
            prev = w
        return math.exp(p)
    #endddef

    
    def getCorpusPerplexity(self, corpus):
        pp = 0.0
        prev = "#"
        for sen in corpus:
            for w in sen:
                if w == start:
                    prev = w
                    continue
                if self.bidict.get(w + " " + prev, 0) == 0:
                    return float("Inf")
                if prev == start:
                    num = self.count
                else:
                    num = self.unidict[prev]
                pp += math.log(self.bidict[w + " " + prev] / num)
                prev = w
        return math.exp(-1 / self.total * pp)
    #enddef
#endclass

#-------------------------------------------
# The main routine
#-------------------------------------------
if __name__ == "__main__":
    #read your corpora
    trainCorpus = readFileToCorpus('train.txt')
    trainCorpus = preprocess(trainCorpus)
    uni =   UnigramModel(trainCorpus)
    smooth = SmoothedUnigramModel(trainCorpus)
    bi = BigramModel(trainCorpus)

    uni.generateSentencesToFile(20,'unigram_output.txt')
    smooth.generateSentencesToFile(20,'smooth_unigram_output.txt')
    bi.generateSentencesToFile(20,'bigram_output.txt')
    
    posTestCorpus = readFileToCorpus('pos_test.txt')
    negTestCorpus = readFileToCorpus('neg_test.txt')

    vocab = set()
    for sen in trainCorpus:
        for word in sen:
            vocab.add(word)
    # Please write the code to create the vocab over here before the function preprocessTest
    print("""Task 0: create a vocabulary(collection of word types) for the train corpus""")
    posTestCorpus = preprocessTest(vocab, posTestCorpus)
    negTestCorpus = preprocessTest(vocab, negTestCorpus)

    print ("POSTIVE")
    print (uni.getCorpusPerplexity(posTestCorpus))
    print (smooth.getCorpusPerplexity(posTestCorpus))
    print (bi.getCorpusPerplexity(posTestCorpus))

    print ("NEGTIVE")
    print (uni.getCorpusPerplexity(negTestCorpus))
    print (smooth.getCorpusPerplexity(negTestCorpus))
    print (bi.getCorpusPerplexity(negTestCorpus))


