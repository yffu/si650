
import nltk
import re, pprint
sentence = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"), ("dog", "NN"), ("barked", "VBD"), ("at", "IN"),  ("the", "DT"), ("cat", "NN")]

grammar= "NP: {<DT>?<JJ>*<NN>}"
cp=nltk.RegexpParser(grammar)
result=cp.parse(sentence)
print result

result.draw()