mkdir -p output
twint -s "#globalwarming OR #emissions OR #climateweeknyc OR #greennewdeal OR #climateball OR #climatehoax OR #co2 OR #climatestrike OR #climateuc" -o "./output/output_8.csv" --lang en --csv --location
echo 'DONE'
READ