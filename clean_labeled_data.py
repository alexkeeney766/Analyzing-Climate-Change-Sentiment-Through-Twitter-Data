import pandas as pd
import os
import random

LOCATION_COLUMN = 'location'
PERCEPTION_COLUMN = 'prediction'

LOCATION_PERCEPTION_OFILE = "cleaned_label_data.csv"
LOCATION_PERCEPTION_HEADERS = ['location', 'positive', 'negative', 'neutral', 'total', 'perception']


write_perception_header=True
def process_loc_perception(date, loc, df):
    global write_perception_header
    loc_data = df.loc[df[LOCATION_COLUMN] == loc]

    data = {
        'date' : date,
        'location': loc,
        'positive': 0,
        'negative': 0,
        'neutral': 0,
        'total': 0,
        'perception': 0
    }

    for _, row in loc_data.iterrows():
        perception = int(row[PERCEPTION_COLUMN])

        if perception == 1:
            data['positive'] += 1
        elif perception == -1:
            data['negative'] += 1
        else:
            data['neutral'] += 1

        data['total'] += 1
        data['perception'] += perception

    location_df = pd.DataFrame(data, index=[0])

    save_data(location_df, LOCATION_PERCEPTION_OFILE, write_perception_header)
    write_perception_header=False

def save_data(df, ofname, write_header):
    df.to_csv(ofname, mode='a', encoding='utf-8', header=write_header, index=False)

def clean_files():
    if os.path.isfile("cleaned_label_data.csv"):
        os.remove("cleaned_label_data.csv")

    if os.path.isfile("location_perception.csv"):
        os.remove("location_perception.csv")

def date_loc_output(data):
    global LOCATION_PERCEPTION_OFILE
    LOCATION_PERCEPTION_OFILE = "cleaned_label_data.csv"

    global write_perception_header
    write_perception_header = True

    dates = data['date'].unique()

    for date in dates:
        date_data = data.loc[data['date'] == date]

        locations = date_data[LOCATION_COLUMN].unique()

        for loc in locations:
            process_loc_perception(date, loc, date_data)

def loc_output(data):
    global LOCATION_PERCEPTION_OFILE
    LOCATION_PERCEPTION_OFILE = "location_perception.csv"

    global write_perception_header
    write_perception_header = True

    locations = data[LOCATION_COLUMN].unique()

    for loc in locations:
        process_loc_perception(None, loc, data)

def main(file):
    clean_files()

    data = pd.read_csv(file)

    # loc_output(data)
    date_loc_output(data)

input_file = "scrubbers/201911281106_unlabeled_merged_data.csv"
if __name__=="__main__":
    import sys

    if len(sys.argv) < 2:
        fname = input_file
    else:
        fname = sys.argv[1]

    try:
        main(fname)
    except:
        print("Usage: python clean_labled_data.py <path_to_labeled_data_csv>")