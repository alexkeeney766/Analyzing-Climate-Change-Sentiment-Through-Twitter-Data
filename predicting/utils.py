import numpy as np
import pandas as pd 
import tensorflow as tf
from tensorflow.python.lib.io.tf_record import TFRecordWriter
import json


def clean_tweets(tweets):
    '''
    Takes the DF defined above and (in this order) applies the following preprocessing steps:
    1. Remove cases
    2. Replaces and URL's with "LINK"
    3. Replaces any twitter handels with "USERNAME"
    4. Removes any punctuation
    
    Note: Stop words will not be removed in this iteration because they may add some information.
    '''
    # Remove cases from the tweets
    tweets = tweets.str.lower()
    
    # Remove URL links
    tweets = tweets.str.replace('http\S+|www.\S+', 'LINK', case = False)
    
    # Remove usernames
    tweets = tweets.str.replace('@.*w', 'USERNAME ', case = False)
    
    # Remove remaining punctuation
    tweets = tweets.str.replace('[^\w\s]', '')
    
    # Convert Stance to a numerical val - Alread done for current DF
    # stances = {'NONE':0, 'AGAINST':-1, 'FAVOR':1}
    # DF.Stance =DF.Stance.map(stances)
    # DF.astype({'Stance': 'int32'}, copy = False)
    return tweets
    
def make_tf_ex(feats, lab):
    tf_ex = tf.train.Example(features = tf.train.Features(feature= {
        'idx' : tf.train.Feature(int64_list = tf.train.Int64List(value = [feats[0]])),
        'sentence' : tf.train.Feature(bytes_list = tf.train.BytesList(value = [feats[1].encode('utf-8')])),
        'label' : tf.train.Feature(int64_list = tf.train.Int64List(value = [lab]))
    }))
    
    return tf_ex


def convert_csv_to_tf_record(csv, file_name):
    writer = TFRecordWriter(file_name)
    for index,row in enumerate(csv):
#         try:
        if row is None:
#             print("row was None")
            continue

        if row[0] is None or row[1] is None:
#             print("row[0] or row[1] was None")
            continue

        if row[0].strip() is '':
#             print("row[0].strip() was ''")
            continue

        feats = (index, row[0])
        lab = row[1]
        example = make_tf_ex(feats, lab)
        writer.write(example.SerializeToString())

#         except Exception as inst:
#             print(type(inst))
#             print(Exception.args)
#             print(Exception.with_traceback)
            
    writer.close()

# def generate_json_info(file_name):
#     info = { "eval_length": len(val) }

#     with open(local_file_name, 'w') as outfile:
#         json.dump(info, outfile)

def read_raw(filename: str, labeled: bool):
    try:
        DF = pd.read_csv(filename)

    except TypeError as t:
        print("wrong file type")
        print(t)

    if labeled:
        tweets = DF.tweet
        labels = DF.prediction.astype('int32')
    else:
        tweets = DF.tweet
        labels = np.zeros((tweets.shape[0])).astype('int')
    
    tweets = clean_tweets(tweets)
    DF = pd.DataFrame(np.array([tweets, labels]).T)
    DF.columns = ['Tweet', 'Stance']
    DF.dropna(inplace = True)
    DF = DF.values

    convert_csv_to_tf_record(DF, f'{filename[:-4]}.tfrecord')


def read_cleaned_csv(filename:str, labeled:bool):
    try:
        DF = pd.read_csv(filename)

    except TypeError as t:
        print("wrong file type")
        print(t)

    if labeled:
        tweets = DF.Tweet
        labels = DF.Stance.astype('int32')
    else:
        tweets = DF.tweet
        labels = np.zeros((tweets.shape[0]))
    
    clean_tweets(tweets)
    DF = pd.DataFrame(np.array([tweets, labels]).T)
    DF.dropna(inplace = True)
    DF = DF.values

    convert_csv_to_tf_record(DF, f'{filename[:-4]}.tfrecord')