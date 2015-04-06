'''
Created on Mar 28, 2015

@author: Yuan-Fang
'''

import nltk, re, csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier

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
        
    #text_clf=text_clf.fit(data, target)
    count_vect=CountVectorizer(ngram_range=(3,3), token_pattern=r'\b\w+\b', min_df=1)
    x_train_counts=count_vect.fit_transform(data)
    #print x_train_counts.shape
    
    tfidf_transformer=TfidfTransformer(use_idf=False)
    x_train_tfidf=tfidf_transformer.fit_transform(x_train_counts)
    #print x_train_tfidf.shape
    
    clf=SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state =42).fit(x_train_tfidf, target)
    
    x_new_counts=count_vect.transform(test_data)
    
    x_new_tfidf=tfidf_transformer.transform(x_new_counts)
    
    predicted=clf.predict(x_new_tfidf)
    
    for doc, category in zip(test_data[:10], predicted[:10]):
        print('%r => %s' % (target_name[category], doc))
        
    with open('data/submission03_svm_tri.csv', 'wb') as hand2:
        writer=csv.writer(hand2, delimiter=',')
        writer.writerow(['Id', 'Category'])
        for tid, category in zip(test_ids, predicted):
            writer.writerow([tid, category])