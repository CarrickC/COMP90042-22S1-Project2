from torchtext.data.utils import get_tokenizer# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 08:47:30 2022

@author: Carrick
"""

import re
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer
import pandas as pd

bert_model = "vinai/bertweet-base"
tokenizer = AutoTokenizer.from_pretrained(bert_model)

class TweetDataset(Dataset):

    def __init__(self, path, seq_len, tokenizer=tokenizer, is_test=False):

        self.df = pd.read_csv(path, delimiter = '\t')
        self.seq_len = seq_len
        self.tokenizer = tokenizer
        self.is_test = is_test

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        
        tweets = self.df.loc[index, 'text']
        
        tweets = self.preprocess(tweets)
        inputs = self.tokenizer(tweets, padding='max_length', truncation=True, return_tensors="pt")
        
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']

        if not self.is_test:
            return input_ids, attention_mask, self.df.loc[index, 'label']
        else:
            return input_ids, attention_mask
    
    def preprocess(self, text):
        # text = re.sub(r'https?://t.co/[a-zA-Z0-9]+', '', text)
        text = text.split('\n')

        if len(text) > self.seq_len:
            text = text[:self.seq_len]
        elif len(text) < self.seq_len:
            text.extend([''] * (self.seq_len - len(text)))

        return text
    
train_set = TweetDataset('../data/train/train.csv', 16)

train_loader = DataLoader(train_set, batch_size = 16, num_workers = 0)

dataiter = iter(train_loader)

tweets, attn_masks, labels = dataiter.next()
