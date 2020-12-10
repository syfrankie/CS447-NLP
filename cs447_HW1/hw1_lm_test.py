from hw1_lm import *

def runTests(modelStr, languageModel, sen, testCorpus):
	print("**** " + modelStr + " ****")
	senProb = 0.0
	testPerp = 0.0
	if modelStr == "unsmoothed_unigram":
		senProb = 0.00384
		testPerp = 6.2544778697
	elif modelStr == "smoothed_unigram":
		senProb = 0.0036730946
		testPerp = 6.3196272719 
	elif modelStr == "unsmoothed_bigram":
		senProb = 0.0
		testPerp = 2.0771150367

	#endif

	print("---TEST: generateSentence()---")
	modelSen = languageModel.generateSentence()
	senTestPassed = False
	if isinstance(modelSen, list):
		if len(modelSen) > 1:
			if isinstance(modelSen[0], str):
				print("pass")
				senTestPassed = True

	#endif
	#endif
	#endif
	if not senTestPassed:
		print("fail; method did not return a list of strings")
	#endif

	print("---TEST: getSentenceProbability()---")
	prob = round(languageModel.getSentenceProbability(sen), 10)
	if prob == senProb:
		print("pass")
	else:
		print("fail; method returned prob of %s, expecting %s" % (str(prob), str(senProb)))
		if modelStr == "smoothed_bigram" and prob == 0.0197842566:
			print("hint: You may be using the unsmoothed unigram model "+\
			"with your smoothed bigram model")
		elif (modelStr == "unsmoothed_unigram" and prob == 0.0002928467) or \
			(modelStr == "smoothed_unigram" and prob == 0.0002817261):
			print("hint: You  may be including the start token in "+\
			  "your distribution and your sentence probability computation")
		elif (modelStr == "unsmoothed_unigram" and prob == 0.0027332362) or \
			(modelStr == "smoothed_unigram" and prob == 0.0026059661):
			print("hint: You may be including the start token in your "+\
			"distribution")
		elif modelStr == "smoothed_bigram" and prob == 0.001516767:
			print("hint: The smoothed unigram model with which you are "+\
			"smoothing your bigram model may include the start token "+\
			"in its distribution")
	#endif
	#endif

	print("---TEST: getCorpusPerplexity---")
	perp = round(languageModel.getCorpusPerplexity(testCorpus), 10)
	if perp == testPerp:
		print("pass")
	else:
		print("fail; method returned perplexity of %s, expecting %s" % (str(perp), str(testPerp)))
		if modelStr == "smoothed_bigram" and perp == 0.6692713234:
			print("hint: You may be using the unsmoothed unigram "+\
			"model with your smoothed bigram model")
		elif (modelStr == "unsmoothed_unigram" and perp == 7.2237390648) or\
			(modelStr == "smoothed_unigram" and perp == 7.2909206567):
			print("hint: You may be including the start token in "+\
			"your distribution and perplexity computation")
		elif (modelStr == "unsmoothed_unigram" and perp == 7.005015214) or\
			(modelStr == "smoothed_unigram" and perp == 7.0856426988):
			print("hint: You may be including the start token in "+\
			"your distribution")
		elif modelStr == "smoothed_bigram" and perp == 2.4614887808:
			print("hint: The smoothed unigram model with which you are "+\
			"smoothing your bigram model may include the start token "+\
			"in its distribution")
	#endif
    #endif
#enddef

if __name__ == '__main__':
	sen = ["<s>", "I", "UNK", "</s>"]
	#sentence = ["<s>", "the", "UNK", "</s>"]

#	get the corpora
	corpus = readFileToCorpus("/Users/syfrankie/Desktop/syfrankie/20fw/447/hw1/cs447_HW1/test.txt") 
	corpus = preprocess(corpus)

	#get your models
	unigram = UnigramModel(corpus)
	smoothedUnigram = SmoothedUnigramModel(corpus)
	bigram = BigramModel(corpus)
	
	#test the models
	
	runTests("unsmoothed_unigram", unigram, sen, corpus)
	runTests("smoothed_unigram", smoothedUnigram, sen, corpus)
	runTests("unsmoothed_bigram", bigram, sen, corpus)

	#endif
