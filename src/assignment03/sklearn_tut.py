'''
Created on Mar 29, 2015

@author: Yuan-Fang
'''

# .rst - the source of the tutorial documents written with Sphinx. 

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

import re

target_name = [ '','Specific disease','Specific treatment','','Family support','Socializing','','Pregnancy','Goal oriented','Demographic-specific']

with open('data/train.csv', 'r') as hand:
    data=list()    
    target=list()
    
    for line in hand:
        match=re.search("^(\d+),(.+)$",line )
        if (match):
            category=int(match.group(1))
            target.append(category)
            text=match.group(2)
            data.append(text)
    for t in target[:10]:
        try:
            print(target_name[t])
        except:
            print "error with ", t
    
    count_vect=CountVectorizer()
    x_train_counts=count_vect.fit_transform(data)
    print x_train_counts.shape
    #print count_vect.vocabulary_.get('algorithm')
    
    tfidf_transformer=TfidfTransformer()
    x_train_tfidf=tfidf_transformer.fit_transform(x_train_counts)
    print x_train_tfidf.shape
    
    clf=MultinomialNB().fit(x_train_tfidf, target)
    
    
'''
each object is a scikit-learn 'bunch', 

target_names = list of category names

files themselves are in data as a list

filename in object.filenames as a list

target contains the numeric category for each posting

to get back the names from the numbers:
    for t in object.target[:10]:
        print(object.target_name[t])

''' 

