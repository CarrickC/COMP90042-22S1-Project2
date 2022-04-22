import requests
import os
import json
import time
import tweepy

# put the file at the same dir as your data folder

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

# change the bearer to your own token
bearer_token = 'AAAAAAAAAAAAAAAAAAAAALEHbwEAAAAAUXzS2ZS5xwPHq%2Bnqh5BKQecyxBg%3DzYRtrv9TCdaByVAqwd9aw442MymSb76LpcfIlZrLHVETMAnYn6'


def create_url(list_of_id):
    tweet_fields = "tweet.fields=attachments,author_id,context_annotations,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld&expansions=referenced_tweets.id"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    ids = "id="+",".join(list_of_id)
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/1.1/statuses/lookup.json?{}".format(ids)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    auth = tweepy.OAuthHandler('KeRDTRZiOf2lSrG9P8GDP5zYI', 'uLqIoNI2RmkVNkDR8IlVn2pfAFzIDKDjUpfJqQb6PRxsdwH494')
    auth.set_access_token('936851572872511489-KJrphbqEukY0e1FteTmilvKFjuF9fwT', '2fHUuJJnkxDNeZpclzEB2RojI3w9CKZpsqqyAoJUmyfnB')
    api = tweepy.API(auth, wait_on_rate_limit = True)
    # change the file address to the id list you want to retrieve
    f = open('data/train/train.data.txt', 'r')
    ids = []
    # read all id from txt
    for line in f.readlines():
        for id in line.strip('\n').split(','):
            ids.append(id)
    # break ids to sublist of 100 tweets per call
    chunks = [ids[x:x+100] for x in range(0, len(ids), 100)]
    i = 0
    for chunk in chunks:
        print(i)
        statuses = api.lookup_statuses(chunk)
        for status in statuses:
            # change the output dir to dir you want to write to
            file_name = 'data/train/tweet_objects/'+status._json['id_str']+'.json'
            with open(file_name, 'w') as outfile:
                outfile.write(json.dumps(status._json, indent=4, sort_keys=True))
        i += 1
    f.close()


if __name__ == "__main__":
    main()