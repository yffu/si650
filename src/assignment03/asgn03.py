'''
Created on Mar 28, 2015

@author: Yuan-Fang
'''

import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

with open('data/train.csv', 'r') as hand:
    for line in hand:
        match=re.search("^(\d+),(.+)$",line )
        if (match):
            print match.group(1), match.group(2)
            tokens=word_ 
        
    