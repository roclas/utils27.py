#!/usr/bin/env python

import nltk,sys


pos_tweets = [('I love this car', 'positive'),
              ('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),
              ('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive')]

neg_tweets = [('I do not like this car', 'negative'),
              ('This view is horrible', 'negative'),
              ('I feel tired this morning', 'negative'),
              ('I am not looking forward to the concert', 'negative'),
              ('He is my enemy', 'negative')]

test_tweets=['I love this chair',
	     'I am tired',
             'You are amazing']

tweets = []
for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
    tweets.append((words_filtered, sentiment))
#print tweets

def get_all_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words
#print get_all_words_in_tweets(tweets) # repiting words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features
allwords=get_all_words_in_tweets(tweets)
word_features=get_word_features(allwords)
#print word_features #all words (no repetition)

def extract_features(document): #extracts the TRAINED words from doc
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

#for t in tweets:
	#print extract_features(allwords)


training_set = nltk.classify.apply_features(extract_features, tweets)
#print training_set
classifier = nltk.NaiveBayesClassifier.train(training_set)



tweet='Larrry is my friend'
print "%s -> %s" %( tweet,classifier.classify(extract_features(tweet.split())))

for t in test_tweets:
	print "%s -> %s" %( t,classifier.classify(extract_features(t.split())))
