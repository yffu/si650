'''
Created on Feb 1, 2015

@author: Yuan-Fang
'''


from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from itertools import groupby
from math import log
import csv, re, os.path
import pprint;

def plot_cnt_freq(filename):
    
    pattern = re.compile("[A-Z]{1}")
    
    summary_stats= dict();
    
    with open ('stoplist.txt') as stops:
        stop_words = [w.strip().lower() for w in stops]
        with open(filename) as blog:
            
            blog_string =blog.read()
            blog_words=word_tokenize(blog_string)
            blog_words.sort()
            # (word, frequency)

            if (os.path.isfile('output/'+filename+'_cap_wdcnt.txt')):
                freq_blog_cap = eval(open('output/'+filename+'_cap_wdcnt.txt', 'r').read())
            else:
                freq_blog_cap= [(key, len(list(group))) for key, group in groupby(blog_words, lambda x: x)]
                
                target = open('output/'+filename+'_cap_wdcnt.txt', 'w')
                target.write(str(freq_blog_cap))
            
            
            if (os.path.isfile('output/'+filename+'_wdcnt.txt')):
                freq_blog = eval(open('output/'+filename+'_wdcnt.txt', 'r').read())
            else:
                freq_blog= [(key, len(list(group))) for key, group in groupby(blog_words, lambda x: x.lower())]
                
                target = open('output/'+filename+'_wdcnt.txt', 'w')
                target.write(str(freq_blog))
            
            # filter out stop words
                
            freq_blog_filtered = [f for f in freq_blog if f[0] not in stop_words]
            
            # vocabulary size
            
            summary_stats["vocabulary size"] = [len(freq_blog), len(freq_blog_filtered) ]
            
            # stopword frequency
            
            stopwd_freq = 0;
            totalwd_freq=0;
            
            for w, cnt in freq_blog:
                if w in stop_words:
                    stopwd_freq += cnt
                totalwd_freq+=cnt
            
            summary_stats["stop frequency"] = stopwd_freq/float(totalwd_freq)
            
            #[f for f in freq_blog if f[0].lower() in stop_words]
            
            # number of capital letters
            
            # average number of character per word
            
            total_chars = 0;
            total_words = 0;
            total_capital = 0;
            
            for word, freq in freq_blog_cap:
                total_chars += len(word)*freq
                total_words += freq
                total_capital += freq * len(pattern.findall(word))
            
            if total_chars != 0 and total_words != 0:
                summary_stats["avg chars per word"] = total_chars/float(total_words)
                summary_stats["number of capital letters"] = total_capital
                
            pos_info = None
            #POS tagging 
            if (os.path.isfile('output/'+filename+'pos_info_uncap.txt')):
                pos_info = eval(open('output/'+filename+'pos_info_uncap.txt', 'r').read())
            else:
                pos_info = pos_tag(word_tokenize(blog_string.lower()))
                target = open('output/'+filename+'pos_info_uncap.txt', 'w')
                target.write(str(pos_info))
                
            pos_counts = dict();
            cross_walk = {'NN': 'noun','JJ': 'adjectives', 'VB': 'verbs', 'RB': 'adverbs', 'PRP': 'pronouns'}
            
            # pos info is unfiltered. 
            
            for word, pos in pos_info:
                pos_type = cross_walk.get(pos);
                if pos:
                    pos_counts[pos_type]=pos_counts.get(pos_type, 0) + 1
                else:
                    None
                    
            summary_stats["POS counts"] = pos_counts
            
            pos_info_sort = sorted (pos_info, key= lambda x: (x[1], x[0]))
            
            pos_word_counts = [(k, len(list(group))) for k, group in groupby(pos_info_sort, lambda x: x )]

            # ((word, pos) counts)    but the problem is that pos does not combine        
            tmp1 = sorted(pos_word_counts, key= lambda x: x[0][1])
            tmp2=[ (k, sorted(group, key= lambda x: x[1], reverse=True)) for k, group in groupby(tmp1, lambda x: x[0][1])]
            
            pos_list , word_count = zip(*tmp2)
            
            topwords_by_pos = dict()
            
            for pos_type in pos_list:
                ts1= word_count[pos_list.index(pos_type)]
                cnt =0
                ts2 =list();
                for word_tup in ts1:
                    if not (cnt < 10):
                        break
                    ts2.append((word_tup[0][0], word_tup[1]))
                    cnt += 1
                topwords_by_pos[cross_walk.get(pos_type)]=ts2
            
            summary_stats["top words by pos"]= topwords_by_pos
                
            freq_blog_sorted=sorted(freq_blog_filtered, key=lambda x: x[1])
            # (frequency, # of unique word)
            cnt_freq_blog = [(key, len(list(group))) for key, group in groupby(freq_blog_sorted, lambda x: x[1])]
            
            log_cnt_freq= [(log(x), log(y)) for x, y in cnt_freq_blog]
            #plt.scatter(*zip(*log_cnt_freq))
            
            #plt.show()
            #print freq_blog_sorted
            #print cnt_freq_blog
        #with open("summary_"+filename, "w") as hand:
        #    a=csv.writer(hand, delimiter = '\t', newline='')
        
        if (os.path.isfile('output/'+filename+'summary.txt')):
            summary = eval(open('output/'+filename+'summary.txt', 'r').read())
        else:
            target = open('output/'+filename+'summary.txt', 'w')
            target.write('output/'+str(summary_stats))

        return summary_stats
    
pp = pprint.PrettyPrinter(indent=4, depth = 10)

        
summary=plot_cnt_freq('blog.txt')
pp.pprint(summary)

summary=plot_cnt_freq('congress_speech.txt')
pp.pprint(summary)