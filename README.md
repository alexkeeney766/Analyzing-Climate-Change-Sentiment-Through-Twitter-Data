# Analyzing Climate Change Stance Through Twitter Data

This project seeks to understand - and visualize - Americans' views of climate change as seen through the lens of twitter. As such, this package 
contains all the resources that were used as we explored different means to classify climate change tweets. 

Below outlines how to recreate our results as accurately as possible, including environment setup, data generation,
model training and scoring, and the post-processing for the final visualization. Given the temporal nature of twitter data, any
attempts at recreating our visualization may not turn out the same. 
 
In order to run a demo of the visualization, with the data that we generated, skip to the [Data Visualization](#data-visualization) section.

This project was originally done as an assignment from Georgia Institute of Technology's Masters of Analytics Program.  It has been since adapted and iterated upon.  The original project was authored by Matt Struble, Daniel Kirel, Silviya Simeonova and myself.  

Tableau Viz: https://public.tableau.com/views/MapandCountchart/Full?:display_count=y&publish=yes&:origin=viz_share_link
 
## Environment Setup

 In order to create a virtual environment and install the necessary libraries, please run the following on a shell:

```
virtualenv venv
source venb/bin/activate
pip install -r requirements.txt
```

 Running `deactivate` should deactivate the virtual environment once you are done working on this.
 
 ### Downloading Labeled Data
 
 Download the following labeled data sources into the `data` directory.
 
 1. https://www.kaggle.com/lextoumbourou/sentiment-of-climate-change
 2. https://www.kaggle.com/edqian/twitter-climate-change-sentiment-dataset
 3. https://raw.githubusercontent.com/edwardcqian/climate_change_sentiment/master/data/sample_data.csv
 
 ## Data Generation 
 
 Our visualization tool relies on live Twitter data, below outlines the various ways of generating the data to be fed to 
 our trained model.
 
 ### 1. Scraping 
 
 Scraping data from Twitter is a very slow process that bypasses Twitter's API limit by scraping the HTML directly. 
 Generating the scraped data and formatting it is a multi-step approach of:
   1. Running the scraping scripts
   2. Consolidating the results
 
 The final product of which is a csv of unlabeled data that can then be fed into our trained model for labeling. 
 
 #### 1. Running the scrapers
 
 Within the `twitter-scrapers` folder exists a number of `scrub_X.sh` scripts which can be run concurrently to scrape
 twitter for different search results, outlined in the table below. Each script can take upwards of days to complete, but
 can be safely stopped at any point and then consolidated. The longer you let the scripts run the more data will be present
 in the final visualization.
 
 | script | search terms |
 | -------|:------------:|
 | scrub_0.sh | #climatefacts, #climatesciencefacts, #climatedenial, #climatetwitter, #carbontax, #climatecult, #changementclimatique, #climatechangethefacts, #climatescience |
 | scrub_1.sh | #climateurgency, #climatesilence, #cleanenergyfuture, #peoplesclimate, #climatedisruption, #naturalclimatesolutions, #climatebudget, #riseforclimate, #endclimatesilence |
 | scrub_2.sh | #climatemarch, #globalclimatestrike, #climat, #environmentaljustice, #climatesolutions, #nofossilfuelmoney, #climatehkh, #parisagreement, "global warming" |
 | scrub_3.sh | #climate, #climateemergency, #climatechangeisreal, #oceanforclimate, #gretathunberg, #climatehope, #climatejustice, #youthstrike4climate, #climatebrawl |
 | scrub_4.sh | #peopleofclimate, #actonclimate, #climatesmart, #startseeingco2, #climateaction, #AGW, #netzero, #strike4climate, #climatechange |
 | scrub_5.sh | #climateservices, #greenhypocrisy, "climate change", #climatehealth, #climatechanged, #climateadaptation, #climatemarxism, #climateresilience, #climatehustle | 
 | scrub_6.sh | #scioclimate, #climatescam, #stateofclimate, #climateactionnow, #climatecrisis, #climatetownhall, #climatefact, #climaterisk, #climatechangeshealth |
 | scrub_7.sh | #climatetutorial, #climatemigration, #up4climate, #youthforclimate, #climateinsurance, #coveringclimatenow, #climatefriday, #climatefinance, #carbonbudget |
 | scrub_8.sh | #globalwarming, #emissions, #climateweeknyc, #greennewdeal, #climateball, #climatehoax, #co2, #climatestrike, #climateuc |
 | scrub_9.sh | #cleanpowerplan, #climateliability, #unclimatesummit, #climatebreakdown |
 
 Separately, the scrape_tweets.py can be used to pull streaming tweets and store them in .txt files.
 
 #### 2. Consolidating the results
 
 Once enough data has been generated the next step is to consolidate the results into a format that is recognizable to our model. 
 This is performed by executing the script `python twitter-scrapers/output_cleaner.py` which:
 * Removes duplicate tweets 
 * Standardizes the date-time format
 * Standardizes csv headings
 * Removes any non-geotagged tweets
 
 
 ### 2. Twitter API

In order to obtain data via the Twitter API, create a `secret_settings.py` file in the `twitter-scrapers` folder with the following content:

```python
twitter_consumer_key = 'XXXXXX'
twitter_consumer_secret = 'XXXXXX'
twitter_access_token = 'XXXXXX'
twitter_access_secret = 'XXXXXX'
```
 
 Once the secret settings have been defined, run the following script `python twitter-scrapers/store_tweets.py`, or `python twitter-scrapers/scrape-tweets.py`.  
 
 Once enough data has been generated by the two files, they can be cleaned up via: 
 
 1. `python twitter-scrapers/consolidate_clean_data.py` is used to consolidate and clean up the `.txt` files produced by `twitter-scrapers/scrape-tweets.py` 
 2. `twitter-scrapers/preprocess_data.ipynb` reformats the tweets into what the models are expecting.
 
 Keep in mind that there is a limit on the number of tweets that can be obtained from the free version of the twitter API. The limits can be found [here](https://developer.twitter.com/en/docs/basics/rate-limiting).

 
 ## Model Training
 
 All BERT model training and testing were done in python notebooks due to the iterative nature of this portion of the project.  We found it necessary to perform frequent sanity checks, which would have been cumbersome in a .py file.  The notebooks allow for viewers to follow along with the same or new data.
 
 The model was trained in 'Modeling_With_BERT.ipynb' and required data formatted as tfrecords. 'Making_TF_records'.ipynb walks through the process of converting data inputted as CSV's to tfrecords. This notebook cleans the data similar to previous models, makes training, testing, and validation data sets, as well as a JSON file that describes the length of each set, and stores them in the data directory.  
 
 With the newly made tfrecord data, the 'Modeling_With_BERT.ipynb' notebook downloads the smaller, uncased, BERT model using the Transformers package: https://huggingface.co/transformers/ . The tfrecord datasets are tokenized in cell 8 using the BERT tokenizer and are converted to batched datasets in the following cell. The model hyper-parameters are set in cell 10, and training happens for three epochs in cell 12.  The rest of the notebook tests the results of the model on the testing dataset; this code is mostly reused in 'Testing_BERT.ipynb'.  
 
 Two python files 'utils.py' and 'classify.py' are included, which give functions that allow for the conversion of CSV files to tfrecord files and classification of new tweets. An example of this can be seen in the 'Labeling.ipynb' notebook

 ## Data Scoring 
 
 Once a model has been trained, datasets can be scored using the following command: `python score_dataset.py <input_file> <output_file>`
 
 ## Data Post-Processing
 
 Once the data has been scored, it then needs to be run through two scripts in order for it to be ready for consumption by our web model. 
 
 
 1. The data needs to be cleaned of any invalid locations. This can be performed by running 
 `python clean_labeled_data.py <path_to_labeled_data.csv>`
 2. The cleaned data needs to go through a final processing step to reformat it into what the web client is expecting. This can be
 performed by running `python process_labeled_data.py`, which should automatically find the `cleaned_labeled_data.csv` file. 
 If not the path to the `cleaned_labeled_data.csv` will need to be passed in via `python process_labeled_data.py <path_to_cleaned_labeled_data.csv>`
 
 Once the new `date_perceptions.csv` file has been generated it can be copied into the `data/states/` directory. 
 
 ## Data Visualization 
 
 The `web/` directory holds everything it needs in order to display the working data visualization. Simply copy the contents of `web/`
 into a webserver, like xampp, and then navigate to the index.html page. A simple way to run locally is to run the following command `python -m http.server 8000` and go to `localhost:8000` on a webrowser.
