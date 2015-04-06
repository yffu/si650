'''
Created on Mar 28, 2015

@author: Yuan-Fang
'''

import nltk, re, csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import MultinomialNB

def ie_preprocess(document):
    sentences=nltk.sent_tokenize(document)
    sentences=[nltk.word_tokenize(sent) for sent in sentences]
    sentences=[nltk.pos_tag(sent) for sent in sentences]
    return sentences
    
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
            print "error with ", t
    
    text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()), ])
    
    parameters={'vect__ngram_range': [(1,1),(1,2)],
                'tfidf__use_idf)': (True, False),
                'clf_alpha' : (1e-2, 1e-3),
                }
    
    gs_clf= GridSearchCV(text_clf, parameters, n_jobs=-1)
    
    gs_clf=gs_clf.fit(data, target)
    
    best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])
    for param_name in sorted(parameters.keys()):
        print("%s: %r" % (param_name, best_parameters[param_name]))
        
    print score
        