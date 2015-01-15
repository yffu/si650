'''
Created on Jan 14, 2015

@author: Yuan-Fang
'''

import ex0101

def invert_matrix(filename):
    matrix = dict();
    result = ex0101.invert(filename);
    
    docs = result[0];
    words = result[1];
    
    print docs 
    print words
    
    for k in words:
        posting = words[k];
        matrix[k]=[1 if (n in posting) else 0 for n in xrange(len(docs))]
        
    for k in matrix:
        print matrix[k], k;
    return [list, matrix];

invert_matrix('../../data/ch01/collection02');