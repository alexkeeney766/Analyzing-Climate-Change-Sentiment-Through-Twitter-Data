mkdir -p output
twint -s "#cleanpowerplan OR #climateliability OR #unclimatesummit OR #climatebreakdown" -o "./output/output_9.csv" --lang en --csv --location
echo 'DONE'
READ