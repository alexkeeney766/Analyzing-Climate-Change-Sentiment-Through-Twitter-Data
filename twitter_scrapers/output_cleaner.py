import pandas as pd
import os
import time
import datetime

LOCATION_COLUMN = 'location'
UID_COLUMN = 'id'

output_data_rows = ['date', 'time', 'timezone', 'user_id', 'tweet', 'hashtags', 'location']

write_header = True

input_dir = 'output'

dataframe_list = []

def remove_duplicate_uid(df):
    data = df.drop_duplicates(subset=[UID_COLUMN])
    print("Removed duplicate uid:", data.shape[0])
    return data

def remove_empty_locations(df):
    data = df[pd.notnull(df[LOCATION_COLUMN])]
    print("Removed empty locations:", data.shape[0])
    return data

def parse_csv(fname):
    data = pd.read_csv(fname)
    print(fname, data.shape[0])
    dataframe_list.append(data)

def combine_dataframes():
    data = pd.concat(dataframe_list, ignore_index=True)
    print('Total rows:', data.shape[0])
    return data


def save_data(df, ofname, write_header):
    df.to_csv(ofname, mode='w', encoding='utf-8', header=write_header, index=False)


def main():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime("%Y%m%d%H%M")

    for file in os.listdir(input_dir):
        fname = os.path.join(input_dir, file)
        if os.path.isfile(fname):
            parse_csv(fname)
    df = combine_dataframes()
    df = df.sort_values(UID_COLUMN, ascending=False)
    df = df.rename(columns={"place":"location"})

    no_dupes = remove_duplicate_uid(df)
    no_empty = remove_empty_locations(no_dupes)

    save_data(no_dupes[output_data_rows], "{}_raw_data.csv".format(st), True)
    save_data(no_empty[output_data_rows], "{}_unlabeled_data.csv".format(st), True)

if __name__=="__main__":
    main()