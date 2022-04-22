import requests
import os
import json

# put the file at the same dir as your data folder

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

# change the bearer to your own token
bearer_token = 'AAAAAAAAAAAAAAAAAAAAALEHbwEAAAAAUXzS2ZS5xwPHq%2Bnqh5BKQecyxBg%3DzYRtrv9TCdaByVAqwd9aw442MymSb76LpcfIlZrLHVETMAnYn6'


def create_url(list_of_id):
    tweet_fields = "tweet.fields=attachments,author_id,context_annotations,created_at,conversation_id,non_public_metrics,organic_metrics,promoted_metrics,reply_settings,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld&expansions=referenced_tweets.id"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    ids = "ids="+list_of_id
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
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
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    # change the file address to the id list you want to retrieve
    f = open('data/dev/dev.data.txt', 'r')
    for line in f.readlines()[:1]:
        ids = line.strip('\n').split(',')
        for id in ids:
            url = create_url(id)
            json_response = connect_to_endpoint(url)
            if 'data' in json_response.keys():
                for obj in json_response['data']:
                    # change the output dir to dir you want to write to
                    file_name = 'data/dev/tweet_objects/'+obj['id']+'.json'
                    with open(file_name, 'w') as outfile:
                        outfile.write(json.dumps(obj, indent=4, sort_keys=True))
    f.close()


if __name__ == "__main__":
    main()