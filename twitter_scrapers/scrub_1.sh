mkdir -p output
twint -s "#climateurgency OR #climatesilence OR #cleanenergyfuture OR #peoplesclimate OR #climatedisruption OR #naturalclimatesolutions OR #climatebudget OR #riseforclimate OR #endclimatesilence" -o "./output/output_1.csv" --lang en --csv --location
echo 'DONE'
READ