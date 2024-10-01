# Dependencies.
# Data.
import pandas as pd
import numpy as np

# Pre-processing.
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
nltk.download("omw-1.4")

# Model.
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Misc.
from difflib import *
from time import sleep, time
import string
import re
import contractions

# ----- HELPER FUNCTIONS -----

def lemmatizeAssist(text):
    '''
    Takes in a string and returns a lemmatized version of the string.
    Uses WordNetLemmatizer and Part of Speech tags to identify words and lemmatize correctly.
    '''
    # Initialize the lemmatizer.
    lemmatizer = WordNetLemmatizer()
    pos_tag_dict = {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV
    }
    
    # Break text into sentences.
    sentences = nltk.sent_tokenize(text)
    lemma_sentences = list()

    # For each sentence, tag the part of speech and use in lemmatizing the word.
    # Add all words to a list, join the list as a new sentence, then save that sentence in 'lemma_sentences'
    for sentence in sentences:
        sentence = sentence.lower()
        new_sentence = list()

        pos_tags = nltk.pos_tag(nltk.word_tokenize(sentence))

        for i, word in enumerate(nltk.word_tokenize(sentence)):
            # Convert POS tag to be compatible with WordNetLemmatizer.
            # When unavailable, run lemmatizer without POS tag.
            nltk_pos = pos_tags[i][1]
            wordnet_pos = pos_tag_dict.get(nltk_pos[0].upper(), None)

            if wordnet_pos is not None:
                new_word = lemmatizer.lemmatize(word, wordnet_pos)
            else:
                new_word = lemmatizer.lemmatize(word)

            new_sentence.append(new_word)

        # Join sentence back together and save.
        new_sentence = " ".join(new_sentence)
        lemma_sentences.append(new_sentence)

    # Return the lemma_sentences combined into a string.
    return " ".join(lemma_sentences)



def processText(text):
    '''
    Takes in a string and returns a processed version of the string using NLTK.
    Expand contractions in the text.
    Lemmatize the text.
    Remove punctuation from the text.
    Remove English stopwords from the text.
    '''
    # Process the text to prepare it for vectorization.
    # 1. Expand contractions.
    text = " ".join([contractions.fix(expanded_word) for expanded_word in text.split()])    

    # 2. Lemmatize.
    text = lemmatizeAssist(text)

    # 3. Remove punctuation.
    text = re.sub('[%s]' % re.escape(string.punctuation), '' , text)
    
    # 4. Remove stopwords.
    text = " ".join([word for word in text.split() if word not in stopwords.words('english')])
    
    # 5. Return the text.
    return text



def columnMerger(row):
    '''
    Combines columns in DataFrame to generate feature text for vectorization.
    Combines columns:
    overview
    genre
    director
    cast1
    cast2
    cast3
    cast4

    Returns a string of the combined information.
    '''
    # Define separate parts of combined string.
    # For cast, iterate through columns 1 thru 4 and grab cast member if exists.
    # Then, add to a combined cast variable.
    # Return the combined string of all variables.
    base_text = row.lemma_text.strip()
    genres = " ".join(row.genre.lower().strip().split(", "))
    director = row.director.lower().strip()

    # Generate cast string.
    all_cast = list()
    for i in range(1, 5):
        cast = row[f'cast{i}']

        if pd.isnull(cast) or cast == '':
            pass
        else:
            all_cast.append(cast.lower().strip())

    all_cast = " ".join(all_cast)

    # ... Done.
    return " ".join([base_text, genres, director, all_cast])