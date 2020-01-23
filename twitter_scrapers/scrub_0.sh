mkdir -p output
twint -s "#climatefacts OR #climatesciencefacts OR #climatedenial OR #climatetwitter OR #carbontax OR #climatecult OR #changementclimatique OR #climatechangethefacts OR #climatescience" -o "./output/output_0.csv" --lang en --csv --location
echo 'DONE'
READ