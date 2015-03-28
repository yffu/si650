'''
Created on Mar 15, 2015

@author: Yuan-Fang
'''

# use anaconda for maylibplot

import matplotlib.pyplot as plt
from itertools import groupby

values = eval(open('result_pl2_processed.txt', 'r').read())

labels = list()

for key in values: 
    
    val = values[key]
    
    zip_vals = zip(*val)
    
    constant = zip_vals[0]
    map_val = zip_vals[1]
    
    plt.plot(constant, map_val, label=key)

plt.ylabel('MAP')
plt.xlabel('PL2_c')
plt.xlim([0,20])
plt.legend()
plt.show()
