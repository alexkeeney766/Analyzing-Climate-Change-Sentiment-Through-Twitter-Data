import sys

import pandas as pd

from predicting.classify import classify
from predicting.utils import clean_tweets, read_raw

if len(sys.argv) != 3:
	print("Must provide an input file and an output file: python score_dataset.py <input_file> <output_file>")

# Load and score dataset
read_raw(sys.argv[1], labeled=False)
y_preds = classify(f'{sys.argv[1][:-4]}.tfrecord')
scoring = pd.read_csv(sys.argv[1])
scoring['prediction'] = y_preds

# Save dataset
scoring.to_csv(sys.argv[2])
