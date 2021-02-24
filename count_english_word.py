import logging
import numpy
from functools import wraps
from collections import Counter
import string
from nltk.corpus import stopwords
from nltk.corpus import words

nltk.download('words')



def clean_tweets(text_list):

    # lowercase
    cleaned_text = [text.lower() for text in text_list]

    # remove \n and \t
    cleaned_text = [text.replace('\n', ' ') for text in text_list]

    # remove special characters
    cleaned_text = [''.join([char for char in text if char not in string.punctuation]) for text in cleaned_text]

    return cleaned_text

def count_english_words(text_list, english_words):

    english_word_counts = []

    for text in text_list:
        # Count all words in text
        words = text.split()
        text_length = len(words)

        counter = [1 if word in english_words else 0 for word in words]

        english_word_counts.append(float(sum(counter) / text_length))




    

if __name__ == '__main__':

    english_words = set(words.word())



