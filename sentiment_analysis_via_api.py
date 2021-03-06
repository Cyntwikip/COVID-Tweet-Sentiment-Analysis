'''Script for performing sentiment analysis from trained model
   or paid cloud APIs.

Usage:
    python sentiment_analysis_via_api.py config.yaml 

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
from tqdm import tqdm
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


def get_sentiment_score_using_google(text_list):
    client = language_v1.LanguageServiceClient()

    texts = []
    text_sentiment = []
    text_score = []

    for text in tqdm(text_list):  
        try:
            document = language_v1.Document(
                content=text,
                type_=language_v1.Document.Type.PLAIN_TEXT,language='en')
            sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

            texts.append(text)
            text_score.append(sentiment.score)
            sentiment_ = 'positive' if sentiment.score > 0 else 'negative' # This is just me
            text_sentiment.append(sentiment_)
        except:
            pass

    return texts, text_sentiment, text_score


# credential=AzureKeyCredential("20c211ec772b4c808c57428e8d1c1105")
# text_analytics_client=TextAnalyticsClient(endpoint="https://sample-senti-analysis.cognitiveservices.azure.com/", credential=credential)

# def get_microsoft_score(text_list):
#     text_score_positive = []
#     text_score_negative = []
#     text_score_neutral = []
#     for text in text_list:
#         response=text_analytics_client.analyze_sentiment([text], language='en')
#         results = [doc for doc in response if not doc.is_error]
#         for doc in results:
#             text_score_positive.append(doc.confidence_scores.positive)
#             text_score_negative.append(doc.confidence_scores.negative)
#             text_score_neutral.append(doc.confidence_scores.neutral) 
#     return text_list, text_score_positive, text_score_negative, text_score_neutral


if __name__ == '__main__' :
    CONFIG_FILE = sys.argv[1]

    with open(CONFIG_FILE) as cfg:
        config = yaml.safe_load(cfg)

    # tweets2019 = pd.read_csv(config['data']['tweets_2019'])
    tweets2020 = pd.read_csv(config['data']['tweets_2020'])

    # text_list_2019 = list(tweets2019['text'])
    # text_list_2019 = text_list_2019[180:190]
    text_list_2020 = list(tweets2020['text'])

    # Use Google Natural Language API
    print('Analyzing sentiment...')
    text_list_, text_sentiment, text_score = get_sentiment_score_using_google(text_list_2020)

    # Save output
    print('Done. Saving...')
    df = pd.DataFrame({
        'text':text_list_,
        'sentiment':text_sentiment,
        'score':text_score})

    df.to_csv(config['output']['google'], index=False)
    print('Saved at {}.'.format(config['output']['google']))

