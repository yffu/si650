'''
Created on Jan 14, 2015

@author: Yuan-Fang
'''

import ex0101


matrix = dict();
result = ex0101.invert('../../data/ch01/collection02');

docs = result[0];
words = result[1];

print docs 
print words

for k in words:
    posting = words[k];
    matrix[k]=[1 if (n in posting) else 0 for n in xrange(len(docs))]
    
for k in matrix:
    print matrix[k], k;