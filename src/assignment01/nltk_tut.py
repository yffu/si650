'''
Created on Feb 1, 2015

@author: Yuan-Fang
'''

from nltk.tokenize import sent_tokenize

sent_tokenize("Hello SF Python, This is NLTK")

sent_tokenize("Hello, Mr. Anderson. We Missed You!")

from nltk.tokenize import word_tokenize

word_tokenize('This is NLTK')

word_tokenize('What\' up?')

# can't resolve import
#from ntlk.tokenize import wordpunct_tokenize

#wordpunct_tokenize('What\' up?')

words = word_tokenize('And now for something totally different')

from nltk.tag import pos_tag

pos_tag(words)

from nltk.chunk import ne_chunk

ne_chunk(pos_tag(word_tokenize('My name is Jacob Perkins.')))

def bag_of_words(words):
    return dict([(word, True) for word in words])

feats = bag_of_words(word_tokenize("great movie"))

import nltk.data

classifier = nltk.data.load('classifiers/movie_reviews_NaiveBayes.pickle')

classifier.classify(feats)


