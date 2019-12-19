import pandas as pd
import os
import random
from location_mapper import states_list

LOCATION_COLUMN = 'location'
PERCEPTION_COLUMN = 'perception'

LOCATION_PERCEPTION_OFILE = "perceptions.csv"
LOCATION_PERCEPTION_HEADERS = ['location', 'positive', 'negative', 'neutral', 'total', 'perception']

location_data = {}
invalid_locations = []

write_perception_header=True
def process_loc_perception(date, loc, df):
    global location_data
    loc_data = df.loc[df[LOCATION_COLUMN] == loc]

    location = ''
    for state in states_list:
        if state == loc:
            location = state.get_state()
            break

    if location == '':
        invalid_locations.append(loc)
        return

    data = {
        'date': date,
        'location': location,
        'positive': int(loc_data['positive']),
        'negative': int(loc_data['negative']),
        'neutral': int(loc_data['neutral']),
        'total': int(loc_data['total']),
        'perception': int(loc_data['perception'])
    }

    if location in location_data:
        location_data[location]['positive'] += data['positive']
        location_data[location]['negative'] += data['negative']
        location_data[location]['neutral'] += data['neutral']
        location_data[location]['total'] += data['total']
        location_data[location]['perception'] += data['perception']
    else:
        location_data[location] = data


def normalize_data(data):
    perception = 0.
    perception += data['positive']/float(data['total'])
    perception += (data['neutral']/float(data['total'])) * 0.5
    data['perception'] = perception

def write_data(data):
    global write_perception_header
    location_df = pd.DataFrame(data, index=[0])

    save_data(location_df, LOCATION_PERCEPTION_OFILE, write_perception_header)
    write_perception_header=False

def save_data(df, ofname, write_header):
    df.to_csv(ofname, mode='a', encoding='utf-8', header=write_header, index=False)

def clean_files():
    if os.path.isfile("perceptions.csv"):
        os.remove("perceptions.csv")

    if os.path.isfile("date_perceptions.csv"):
        os.remove("date_perceptions.csv")

def loc_output(data):
    global LOCATION_PERCEPTION_OFILE
    LOCATION_PERCEPTION_OFILE = "perceptions.csv"

    global write_perception_header
    write_perception_header = True

    locations = data[LOCATION_COLUMN].unique()

    for loc in locations:
        process_loc_perception(None, loc, data)

    for location in location_data.keys():
        normalize_data(location_data[location])
        write_data(location_data[location])



def date_loc_output(data):
    global LOCATION_PERCEPTION_OFILE
    global location_data
    LOCATION_PERCEPTION_OFILE = "date_perceptions.csv"

    global write_perception_header
    write_perception_header = True

    dates = data['date'].unique()

    for date in dates:
        date_data = data.loc[data['date'] == date]

        locations = date_data[LOCATION_COLUMN].unique()

        for loc in locations:
            process_loc_perception(date, loc, date_data)

        for location in location_data.keys():
            normalize_data(location_data[location])
            write_data(location_data[location])

        location_data.clear()

def main(file):
    clean_files()

    data = pd.read_csv(file)

    # loc_output(data)
    date_loc_output(data)


input_file = "cleaned_label_data.csv"
if __name__=="__main__":
    import sys

    if len(sys.argv) < 2:
        fname = input_file
    else:
        fname = sys.argv[1]

    try:
        main(fname)
    except:
        print("Usage: python process_labeled_data.py <path_to_cleaned_labeled_csv>")