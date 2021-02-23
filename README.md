# COVID-Tweet-Sentiment-Analysis

This repository uses the tweet data I have collected using the Twitter Premium API. The tweet data contains all the tweets from the "top 30 users" who tweeted the most about `COVID` in the National Capital Region of the Philippines from March 9, 2020 (1 week before lockdown) to March 22, 2020 (1 week after start of lockdown). The top 30 users were determined by obtaining the users with most tweet counts from another twitter API query--query that retrieves all tweets with `COVID` in the same location and time period. 

See the <a href="https://twittercommunity.com/t/twitter-data-and-counts-endpoints-mismatch/146719">following post on Twitter forums</a> for the query I used (just change the date) and its nuances to collect the prerequisite data. I personally asked that question due to the discrepancy in the results.

The `top users` folder contains the top 30 users tweet data in JSON format. In addition, there are also scripts to parse the said file and also calculate the sentiment score of each tweet in it. To get you started, read and run the following files in order:
1. `top-user-tweets-parser.ipynb` - parses the data, and saves the relevant data into CSV format 
2. `top-user-sentiments.ipynb` - calculates the sentiments and token-used ratio of each tweet.
3. `sentiment_analysis_via_api.api` - calculates sentiments using the Google Cloud Natural Language API. Saves output in `csv` format. 