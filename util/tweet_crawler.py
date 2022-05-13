import tweepy
import os
import configparser
import json


def config():
    config = configparser.RawConfigParser()
    # Put your keys and tokens in file config.ini under the same dir
    config.read('config.ini')
    return (config['twitter']['api_key'], 
            config['twitter']['api_key_secret'], 
            config['twitter']['access_token'],
            config['twitter']['access_token_secret'])

def get_api():
    key, key_secret, access_token, access_token_secret = config()
    auth = tweepy.OAuth1UserHandler(key, key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)    
    
    return api


def main():
    api = get_api()
    # file = open('data/train/train.data.txt', 'r')
    # file = open('data/dev/dev.data.txt', 'r')
    file = open('../data/covid/covid.data.txt', 'r')
    lines = file.readlines()
    start = 0
    tweet_ids = []
    tweet_count = 0
    for line in lines[start:]:
        line = line.replace('\n', '').split(',')
        for tweet_id in line:
            tweet_ids.append(tweet_id)
            if len(tweet_ids) == 100:
                tweets = api.lookup_statuses(tweet_ids)
                for i in range(len(tweets)):
                    tweet = tweets[i]
                    # path = 'data/train/tweet_objects/' + tweet.id_str + '.json'
                    # path = 'data/dev/tweet_objects/' + tweet.id_str + '.json'
                    path = '../data/covid/tweet_objects/' + tweet.id_str + '.json'
                    # if hasattr(tweet, 'text'):
                    jsonf = open(path, 'w+', encoding='utf-8')
                    json.dump(tweet._json, jsonf, ensure_ascii=False, indent=4)
                    jsonf.close()
                    print('{} {}'.format(tweet_count, tweet_ids[i]))
                    # else:
                    #     print('{} {} Not avaliable'.format(tweet_count, tweet_ids[i]))
                    #     if os.path.isfile(path):
                    #         os.remove(os.path.join(path))
                    tweet_count += 1
                
                    
                tweet_ids.clear()
                
    tweets = api.lookup_statuses(tweet_ids)
    for i in range(len(tweets)):
        tweet = tweets[i]
        # path = 'data/train/tweet_objects/' + tweet_ids[i] + '.json'
        path = '../data/covid/tweet_objects/' + tweet.id_str + '.json'
        # if hasattr(tweet, 'text'):
        jsonf = open(path, 'w+', encoding='utf-8')
        json.dump(tweet._json, jsonf, ensure_ascii=False, indent=4)
        jsonf.close()
        print('{} {}'.format(tweet_count, tweet_ids[i]))
        # else:
        #     print('{} {} Not avaliable'.format(tweet_count, tweet_ids[i]))
        #     if os.path.isfile(path):
        #         os.remove(os.path.join(path))
    
        tweet_count += 1
    tweet_ids.clear()
    


if __name__ == "__main__":
    main()