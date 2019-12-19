import tensorflow as tf 
import json 
# from transformers import *
from transformers import BertTokenizer, TFBertForSequenceClassification, glue_convert_examples_to_features
from transformers.configuration_bert import BertConfig

# Model components
def classify(fname:str, verbose:bool = False):
    '''
    Returns a 1 dimensional numpy array of predictions
    Currently predictions 0, -1, 1 are indexed at 0, 1, 2
    Therefore when reading the return array:
    0 = 'Neutral', 1 = 'Deny', 2 = 'Favor'
    '''
    tokenizer = BertTokenizer('../models/BERT-vocab1.dms')
    config = BertConfig.from_json_file('../models/BERT-config0.json')
    model = TFBertForSequenceClassification.from_pretrained('../models/BERT-transfer1/', config = config)

    # BATCH_SIZE = 64
    feat_spec = {
        'idx' : tf.io.FixedLenFeature([], tf.int64),
        'sentence' : tf.io.FixedLenFeature([], tf.string),
        'label' : tf.io.FixedLenFeature([], tf.int64)
    }

    def parse_ex(ex_proto):
        return tf.io.parse_single_example(ex_proto, feat_spec)

    tweets = tf.data.TFRecordDataset(fname)
    tweets = tweets.map(parse_ex)

    # with open('data/tweet_info.json')as j_file:
    #     data_info = json.load(j_file)
    #     num_samples = data_info['DF_length']

    eval_df = glue_convert_examples_to_features(examples = tweets,
                                                tokenizer = tokenizer,
                                                max_length = 128,
                                                task = 'sst-2',
                                                label_list = ['0','-1', '1'])
    eval_df = eval_df.batch(64)

    y_preds = model.predict(eval_df, use_multiprocessing=True, verbose = verbose)
    y_preds_sm = tf.nn.softmax(y_preds)
    y_preds_argmax = tf.math.argmax(y_preds_sm, axis = 1)
    return y_preds_argmax.numpy()