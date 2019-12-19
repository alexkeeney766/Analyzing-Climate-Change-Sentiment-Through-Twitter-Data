import sys
import json

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

sys.path.append('../predicting')
from predicting.classify import classify
from predicting.ensemble_classifier import VoteClassifier
from twitter_scrapers.secret_settings import *


class tweepy_listener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)['text'].translate(non_bmp_map)
        sentiment, confidence = vote_classifier.predict(tweet)

        print(tweet, sentiment, confidence)

        if confidence >= 0.8:
            output = open('twitter_sentiment.txt', 'a')
            output.write(sentiment + '\n')
            output.close()
            
        return True

    def on_error(self, status):
        print(status)


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

vote_classifier = VoteClassifier()

vote_classifier.load('models/ensemble.p')

oauth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
oauth.set_access_token(twitter_access_token, twitter_access_secret)

open('twitter_sentiment.txt', 'w').close()
twitterStream = Stream(oauth, tweepy_listener())
twitterStream.filter(track=['climate change'])

