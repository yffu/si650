'''
Created on Mar 15, 2015

@author: Yuan-Fang
'''

#import matplotlib.pyplot as plt
import BeautifulSoup as bs

with open('results_3_pl2.html','r') as hand:
    
    content = hand.read()
    soup = bs.BeautifulSoup(content)
    
    values = dict()
    
    headers=list()
    cnt = 0
    for h1 in soup.findAll('h1'):
        if (cnt == 0 ):
            cnt += 1
            continue
        headers.append(h1.contents[0])
    
    cnt =0
    for t in soup.findAll('table'):
        for tr in t.contents[2].findAll('tr'):
            row_val = list()
            for td in tr.findAll('td'):
                row_val.append(td.contents[0])
            if values.get(headers[cnt]) == None:
                values[headers[cnt]]= list()
            values[headers[cnt]].append(row_val)
        cnt = cnt+1
        print cnt
    print values

    with open('result_pl2_processed.txt', 'w') as hand2:
        hand2.write(str(values))