'''
Created on Mar 28, 2015

@author: Yuan-Fang
'''

import nltk, re, csv, random


import logging
import numpy as np
from optparse import OptionParser
import sys
from time import time
import matplotlib.pyplot as plt

from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn import metrics

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

def ie_preprocess(document):
    sentences=nltk.sent_tokenize(document)
    sentences=[nltk.word_tokenize(sent) for sent in sentences]
    sentences=[nltk.pos_tag(sent) for sent in sentences]
    return sentences

def benchmark(clf):
    print("Training ", clf)
    clf.fit(X_train, y_train)
    print ("train done")
    pred=clf.predict(X_test)
    print ("test done")
    
    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)
    
    clf_descr = str(clf).split('(')[0]
    return clf_descr, score
    
target_name = [ '','Specific disease','Specific treatment','','Family support','Socializing','','Pregnancy','Goal oriented','Demographic-specific']

with open('data/train.csv', 'r') as hand:
    data=list()    
    target=list()
    
    test_data=list()
    test_ids=list()
    
    with open('data/test.csv', 'r') as hand1:
        for l in hand1:
            match=re.search("^(\d+),(.+)$", l)
            if (match):
                text_id=match.group(1)
                test_ids.append(text_id)
                text=match.group(2)
                test_data.append(text)        
    
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
            print("error with ", t)
    
    # split a training set and a test set.
    
    train_vals=zip(data, target)
    random.shuffle(train_vals)
    
    x_train, y_train = zip(*train_vals[2*len(train_vals)/3:])
    x_test, y_test = zip(*train_vals[:2*len(train_vals)/3])
        
    for i in range(10):
        print('train vals', x_train[i], y_train[i])
        print('test vals', x_test[i], y_test[i])
        
        
    print ("extracting features from the training data using sparse vectorizer")
    
    # other options ngram_range=(3,3)
    
    count_vect=CountVectorizer(tokenizer=LemmaTokenizer(), stop_words='english')
    
    x_train_cnt = count_vect.fit_transform(x_train)
    
    x_test_cnt = count_vect.transform(x_test)
    
    tfidf_transformer=TfidfTransformer(sublinear_tf=True, use_idf=True, norm='l2')
    
    X_train=tfidf_transformer.fit_transform(x_train_cnt)
    
    print("n_samples: %d, n_features: %d" % X_train.shape)
    
    print()
    
    print("Extracting features from the test data using the same vectorizer")
    
    X_test = tfidf_transformer.transform(x_test_cnt)
    
    print("n_samples: %d, n_features: %d" % X_test.shape)
    
    print()
    
    # mapping from integer feature name to original token string
    
    feature_names = count_vect.get_feature_names()
    
    print (len(feature_names))
    
    ch2 = SelectKBest(chi2, k=7000)
    
    X_train = ch2.fit_transform(X_train, y_train)
    
    X_test = ch2.transform(X_test)

    if feature_names:
        # keep selected feature names
        feature_names = [feature_names[i] for i
                     in ch2.get_support(indices=True)]
    
    print(len(feature_names))
    
    # these are the features found by the chisquared method used in the X-train. 
    
    if feature_names:
        feature_names=np.asarray(feature_names)
        
            
    for clf, name in (
            (RidgeClassifier(tol=1e-2, solver="lsqr"), "Ridge Classifier"),
            (Perceptron(n_iter=50), "Perceptron"),
            (PassiveAggressiveClassifier(n_iter=50), "Passive-Aggressive"),
            (KNeighborsClassifier(n_neighbors=10), "kNN"),
            (RandomForestClassifier(n_estimators=100), "Random forest")):
        benchmark(clf)
        
    benchmark(SGDClassifier(alpha=.0001, n_iter=50,
                                       penalty="elasticnet"))
    
    benchmark(NearestCentroid())
    
    benchmark(MultinomialNB(alpha=.01))
    
    benchmark(BernoulliNB(alpha=.01))
    
    benchmark(Pipeline([
    ('feature_selection', LinearSVC(penalty="l1", dual=False, tol=1e-3)),
    ('classification', LinearSVC())
    ]))
            
    '''
    
    #count_vect=CountVectorizer(ngram_range=(3,3), min_df=1)
    x_train_counts=vectorizer.fit_transform(data)
    #print x_train_counts.shape
    
    tfidf_transformer=TfidfTransformer(use_idf=False)
    x_train_tfidf=tfidf_transformer.fit_transform(x_train_counts)
    #print x_train_tfidf.shape
    
    clf=SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state =42).fit(x_train_tfidf, target)
    
    x_new_counts=vectorizer.transform(test_data)
    
    x_new_tfidf=tfidf_transformer.transform(x_new_counts)
    
    predicted=clf.predict(x_new_tfidf)
    
    for doc, category in zip(test_data[:10], predicted[:10]):
        print('%r => %s' % (target_name[category], doc))
        
    with open('data/submission03_svm_tri.csv', 'wb') as hand2:
        writer=csv.writer(hand2, delimiter=',')
        writer.writerow(['Id', 'Category'])
        for tid, category in zip(test_ids, predicted):
            writer.writerow([tid, category])
            
    '''