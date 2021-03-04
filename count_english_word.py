import logging
import pandas as pd
import numpy
from functools import wraps
from collections import Counter
import string
import nltk
from nltk.corpus import stopwords
from nltk.corpus import words

nltk.download('words')


def clean_tweets(text_list):

    # lowercase
    cleaned_text = [text.lower() for text in text_list]

    # remove \n and \t
    cleaned_text = [text.replace('\n', ' ') for text in cleaned_text]

    # remove special characters
    cleaned_text = [''.join([char for char in text if char not in string.punctuation]) for text in cleaned_text]

    return cleaned_text

def count_english_words(text_list, english_words):

    total_word_counts = []
    english_word_count = []
    english_word_proportion = []

    for text in text_list:
        # Count all words in text
        words = text.split()
        text_length = len(words)

        # Find word in wordnet
        counter = [True if word in english_words else False for word in words]
        num_word_recognized = sum(counter)
        # print(counter)
        # print(words)
        # print(sum(counter))

        total_word_counts.append(text_length)
        english_word_count.append(num_word_recognized)
        english_word_proportion.append(float(num_word_recognized / text_length))
    
    return total_word_counts, english_word_count, english_word_proportion



    

if __name__ == '__main__':

    english_words = set(words.words())
    print('Length english words', len(english_words))

    tweets2019 = pd.read_csv('top_tweets_2019_03.csv')
    tweets2020 = pd.read_csv('top_tweets_2020_03.csv')

    tweets = pd.concat([tweets2019, tweets2020])
    tweet_list = list(tweets['text'])

    print('Cleaning text...')
    cleaned_tweets = clean_tweets(tweet_list)

    print('Counting words...')
    tweet_length, eng_words_recognized, english_word_ratio = count_english_words(cleaned_tweets, english_words)

    print('Saving table...')
    english_count_df = pd.DataFrame(
        {
        'text' : tweet_list,
        'cleaned_text' : cleaned_tweets,
        'tweet_length' : tweet_length,
        'eng_words_recognized' : eng_words_recognized,
        'english_word_count' : english_word_ratio
        }
    )

    english_count_df.to_csv('english_word_counts.csv', index=False)
    print('Done.')
