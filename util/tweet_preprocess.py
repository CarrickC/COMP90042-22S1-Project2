# -*- coding: utf-8 -*-
"""
Created on Tue May  3 10:29:29 2022

@author: Carrick
"""

import re
import string
import pandas as pd


def preprocess(text):
    
    # Lowercase
    text = text.lower()
    
    # Remove mention
    # text = re.sub(r"@\S+", "", text)
    text = re.sub(r"@", "", text)
    
    # Remove URL
    text = re.sub(r'http\S+', 'http', text)
    
    # Remove punctuation and digits
    text = text.translate(str.maketrans(dict.fromkeys(string.punctuation+string.digits, '')))
    
    # Remove non ascii char
    text = re.sub(r'[^\x00-\x7F]', '', text)
    
    # Remove redundant space
    text = re.sub(r' +', ' ', text)
    text = [t.strip() for t in text.split('\n') if t.strip() != '']
    text = '\n'.join(text)
    
    return text

# path = r'D:\学习\Unimelb\COMP90042\Project\Rumour-Detection-and-Analysis-on-Twitter\data\train\train.csv'
# df = pd.read_csv(path, delimiter = '\t')

