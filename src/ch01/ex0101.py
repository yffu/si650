'''
Created on Jan 13, 2015

@author: root
'''

import os, csv

def invert(filename):
    pairs = list();
    docs = dict();
    
    with open(filename, 'r') as in_hand:
        cnt = 0;
        for line in csv.reader(in_hand, delimiter = '\t'):
            if (len(line) < 2):
                break;
            docs[cnt]=line[0];
            for word in line[1].split():
                pairs.append((word, cnt));
            cnt +=1;
    pairs = sorted(pairs, key=lambda pair: pair[0]);
    #print pairs;
    
    tmp = '';
    
    words = dict();
    for pair in pairs:
        if (pair[0] == tmp):
            words[pair[0]].append(pair[1]);
        else:
            words[pair[0]] = [pair[1]];
        tmp = pair[0];
    
    return (docs, words);

result = invert('../../data/ch01/collection01');
print result[0];
print result[1];