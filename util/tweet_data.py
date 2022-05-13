import os
import re
import json
import pandas as pd
import numpy as np
from tweet_preprocess import preprocess

root = '../data/train/'
dtype = 'train'

ids_path = root + dtype + '.data.txt'
ids_file = open(ids_path, 'r')
ids_lines = ids_file.readlines()
label_path = root + dtype + '.label.txt'
label_file = open(label_path, 'r')
label_lines = label_file.readlines()
assert len(ids_lines) == len(label_lines)

data = []


for ids, label in zip(ids_lines, label_lines):
# for ids in ids_lines:
    tweets_seq = ''
    ids = ids.replace('\n', '').split(',')
    label = label.replace('\n', '')
    
    # source_tweet = ''
    
    for i in range(len(ids)):
        tid = ids[i]
        path = root + 'tweet_objects/' + tid + '.json'
        
        
        if os.path.isfile(path):
            tweet_json = open(path, 'r', encoding='UTF-8')
            tweet = json.load(tweet_json)
            tweet_json.close()
            if i == 0:
                if tweet['text'] == '':
                    break
                tweets_seq += tweet['text'] + '\n'
            
            if tweet['text'] != '':
                if i != len(ids)-1:
                    tweets_seq += tweet['text'] + '\n'
                else:
                    tweets_seq += tweet['text']
                
    if tweets_seq != '':
        # data.append([tweets_seq])
        data.append([tweets_seq, 1 if label == 'rumour' else 0])
        # data.append(['{} {}'.format(source_tweet, tweet['text']), 1 if label == 'rumour' else 0])
    
    
df = pd.DataFrame(data, columns = ['text', 'label'])
# df = pd.DataFrame(data, columns = ['text'])

# df['text'] = df['text'].apply(lambda text: preprocess(text))
df['text'].replace('', np.nan, inplace=True)
df.dropna(subset=['text'], inplace=True)

# df.to_csv(root + dtype + '.csv', sep='\t', index=False, encoding='utf-8')