# References: http://adilmoujahid.com/posts/2014/07/twitter-analytics/

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from secret_settings import *

access_token = twitter_access_token
access_token_secret = twitter_access_secret
consumer_key = twitter_consumer_key
consumer_secret = twitter_consumer_secret


#This prints received tweets to stdout.
class Listener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # Twitter authetification and connection to Twitter Streaming API
    l = Listener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # Filter Twitter streams by specified keywords
    stream.filter(track=['climate change','global warming','#climatechange', '#globalwarming', \
                         '#climate','#climatestrike','#climatebrawl','#climatecrisis', \
                         '#climatehoax','#climateemergency','#climatescam','#climatecult', \
                         '#climateaction','#climatechangeisreal','#nolifewithoutco2','#fossilfuels', \
                         '#co2gasoflife','#gretathunberg','#lifewantsmoreco2','#ipcc', \
                         '#greennewdeal','#actonclimate','#climateaction','#fridaysforfuture', \
                         '#parisagreement','#climatedebate','#sustainability', \
                         '#climatetownhall','#climatemarch','#earthday','#climatehope', \
                         '#climatejustice'])                