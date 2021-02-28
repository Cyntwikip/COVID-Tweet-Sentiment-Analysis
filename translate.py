import googletrans
from googletrans import Translator
from google_trans_new import google_translator
import nltk
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import random
import pandas as pd
from sentiment_analysis_via_api import get_sentiment_score_using_google
from collections import Counter

nltk.download('vader_lexicon')


def translate_text_list(text_list):
    translator = Translator()
    text_translated = []
    translations = translator.translate(text_list)

    for translation in translations:
        text_translated.append(translation.text)

    return text_list, text_translated

def translate_text_list_1(text_list):
    'googletrans appears to have a bug right now.'

    translator = google_translator()
    translations = translator.translate(text_list)

    return text_list, translations

def get_words_not_translated(text_translated):

    untranslated_words = []

    for text in text_translated:
        for word in text:
            if word not in english_words:
                untranslated_words.append(word)
    
    return untranslated_words


# lagay ung google at vader scores sa csv before loading
# get tweets with low english word ratio
df = pd.read_csv('tweets_all_stats.csv')
df_low_english = df[df['english_word_count'] < 0.20]

# generate random index
random.seed(10)
num_sample = 500
indices = random.sample(range(len(df_low_english)), num_sample)
df_to_translate = df_low_english.iloc[indices,:]

# translate to english
text_to_translate = list(df_to_translate['text'].copy())
_, text_translated = translate_text_list(text_to_translate)

# get sentiments from Google NL, VADER, MS Text Analytics

# Google NL
text_translated_, text_sentiment, text_google_scores = get_sentiment_score_using_google(text_translated)

# VADER
analyzer=SentimentIntensityAnalyzer()
text_vader_scores = []

for text in text_translated:
    temp_score = analyzer.polarity_scores(text)
    text_vader_scores.append(temp_score['compound'])

# MS Text Analytics

# Append scores to df_to_translate
df_to_translate['text_translated'] = text_translated
df_to_translate['new_vader_score'] = text_vader_scores
df_to_translate['new_google_score'] = text_google_scores

# Then create viz and stats on `token_stats.ipynb`

# Get words that are not in WordNet
english_words = set(words.words())
un_translated_words = []
for text in text_translated:
    for word in text.split:
        if word not in english_words:
            un_translated_words.append(word)

# Try to get counts?
untranslated_counts = Counter(un_translated_words)

# Bar chart ng most frequent
# Then word cloud para makasama ung mga infrequent words









