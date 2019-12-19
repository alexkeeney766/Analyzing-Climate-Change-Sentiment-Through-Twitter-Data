import json
import pandas as pd
import glob, os
import numpy as np

files = []

# Consolidate all .txt files containing data pulled from Twitter
os.chdir('path to directory with .txt files pulled with scrape_tweets.py')
for file in glob.glob('*.txt'):
    files.append(file)

tweets_data = []

for file in files:
    tweets_file = open(file, "r")
    
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    
print(len(tweets_data))

data = pd.DataFrame()

data['created_at'] = [t['created_at'] for t in tweets_data]
data['timezone'] = [t['user']['time_zone'] for t in tweets_data]
data['user_id'] = [t['id'] for t in tweets_data]
data['text'] = [t['text'] for t in tweets_data]
data['truncated'] = [t['truncated'] for t in tweets_data]

for t in tweets_data:
    if 'extended_tweet' not in list(t.keys()):
        t['extended_tweet'] = {}
        if 'full_text' not in list(t['extended_tweet'].keys()):
            t['extended_tweet']['full_text'] = ''  
    if 'retweeted_status' not in list(t.keys()):
        t['retweeted_status'] = {}
        if 'text' not in list(t['retweeted_status'].keys()):
            t['retweeted_status']['text'] = ''
        if 'truncated' not in list(t['retweeted_status'].keys()):
            t['retweeted_status']['truncated'] = ''
    if 'extended_tweet' not in list(t['retweeted_status'].keys()):
        t['retweeted_status']['extended_tweet'] = {}
        if 'full_text' not in list(t['retweeted_status']['extended_tweet'].keys()):
            t['retweeted_status']['extended_tweet']['full_text'] = ''

        
data['extended_text'] = [t['extended_tweet']['full_text'] for t in tweets_data]
data['RT_text'] = [t['retweeted_status']['text'] for t in tweets_data]
data['RT_truncated'] = [t['retweeted_status']['truncated'] for t in tweets_data]
data['extended_RT_text'] = [t['retweeted_status']['extended_tweet']['full_text'] for t in tweets_data]

data['location'] = [t['user']['location'] for t in tweets_data]
data['location'].replace('', np.nan, inplace=True)
data.dropna(subset=['location'], inplace=True)

data.to_csv(r'path to desired location of consolidated data')
print('Done!')
