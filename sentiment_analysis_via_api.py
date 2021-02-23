'''Script for performing sentiment analysis from trained model
   or paid cloud APIs.

Usage:
    python sentiment_analysis_via_api.py config.py 

Author:
    Cedric Basuel

Notes:
    If using the Google API, set env variables in terminal first.
    For example: `export GOOGLE_APPLICATION_CREDENTIALS="/Users/service_key.json"`

References:
    Google natural language api: 
        https://cloud.google.com/natural-language/docs/basics#interpreting_sentiment_analysis_values
    Microsoft text analytics api:
        https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/how-tos/text-analytics-how-to-sentiment-analysis?tabs=version-3-1
'''

import sys
import yaml
from google.cloud import language_v1
import pandas as pd
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


def get_sentiment_score_using_google(text_list):
    client = language_v1.LanguageServiceClient()

    text_sentiment = []
    text_score = []

    for text in text_list:  
        document = language_v1.Document(content=text,type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        text_score.append(sentiment.score)

        sentiment_ = 'positive' if sentiment.score > 0 else 'negative' # This is just me
        text_sentiment.append(sentiment_)

    return text_list, text_sentiment, text_score


if __name__ == '__main__' :
    CONFIG_FILE = sys.argv[1]

    with open(CONFIG_FILE) as cfg:
        config = yaml.safe_load(cfg)

    tweets2019 = pd.read_csv(config['data']['tweets_2019'])
    # tweets2020 = pd.read_csv(config['data']['tweets_2020'])

    text_list_2019 = list(tweets2019['text'])
    text_list_2019 = text_list_2019[0:10]
    # text_list_2020 = list(tweets2020['text'])

    # Use Google Natural Language API
    text_list_, text_sentiment, text_score = get_sentiment_score_using_google(text_list_2019)

    # Save output
    df = pd.DataFrame({
        'text':text_list_,
        'sentiment':text_sentiment,
        'score':text_score})

    df.to_csv(config['output']['google'], index=False)


