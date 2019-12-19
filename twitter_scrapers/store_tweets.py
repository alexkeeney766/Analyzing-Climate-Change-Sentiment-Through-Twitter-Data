import sys
import csv

from tweepy import API, OAuthHandler, Cursor

from secret_settings import *
from twitter_query import query


oauth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
oauth.set_access_token(twitter_access_token, twitter_access_secret)

api = API(oauth)

# Open/create a file to append data to
with open('data/tweets.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')

    for tweet in Cursor(api.search, q=query, lang='en').items(10000):
        text = tweet.text.translate(non_bmp_map)
        cleaned = ''.join([c for c in text if ord(c) < 128])

        writer.writerow([cleaned, tweet.user.location, tweet.created_at])
        # print(tweet.created_at, text)
