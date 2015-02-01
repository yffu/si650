'''
Created on Feb 1, 2015

@author: Yuan-Fang
'''
import os.path, matplotlib.pyplot as plt, pprint

pp = pprint.PrettyPrinter(indent=4)

def plotter(filenames):
    #cross_walk = {'NN': 'noun','JJ': 'adjectives', 'VB': 'verbs', 'RB': 'adverbs', 'PRP': 'pronouns'}
    summary_info = list();
    for f in filenames: 
      
        if (os.path.isfile(f+'summary.txt')):
            summary_info.append(eval(open(f+'summary.txt', 'r').read()))
        else:
            return
        
    
    hand =open('summary_pp.txt', 'w')
    hand.write(str(pp.pprint(summary_info)))
    hand.close()
    
    #plt.scatter()
    #plt.show()

plotter(['blog.txt', 'congress_speech.txt'])
