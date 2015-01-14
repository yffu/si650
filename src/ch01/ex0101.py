'''
Created on Jan 13, 2015

@author: root
'''

import os, csv

pairs = list();
docs = dict();

with open('../../data/collection01', 'r') as in_hand:
    cnt = 0;
    for line in csv.reader(in_hand, delimiter = '\t'):
        if (len(line) < 2):
            break;
        docs[cnt]=line[0];
        for word in line[1].split():
            pairs.append((word, cnt));
        cnt +=1;
pairs = sorted(pairs, key=lambda pair: pair[0]);
print pairs;
# for pair in pairs:
    
        
        