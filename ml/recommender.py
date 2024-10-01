# ... // what it doooo babey


# perform check on inputted user movie
# if exists, use that as target,
# if not, movie_processor will take care of it and get us a row


# Dependencies.
# Data.
import pandas as pd
import numpy as np

# Model.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Request.
from movie_processor import getMovie

# Misc.
from difflib import *

def recommend(list_length, movie_dict):
    '''
    Recommend a list of movies based on user input.
    Input is a dictionary containing keys 'name' and optionally, 'feature'.
    User input it used to generate TFIDF matrix with our movie dataset.
    Recommendations are listed based on the cosine similarity of the TFIDF matrix.
    Returns a dictionary with the results of the search.
    '''
    
    # Load the dataset.
    df = pd.read_csv("resources/ml_movie.csv", index_col = False)

    # Find if using KEYWORDS or TITLE.
    if movie_dict['name'] == "KEYWORDS":
        df_n = pd.DataFrame(
            movie_dict,
            columns = ['title', 'feature'],
            index = [0]
        )

        df = pd.concat([df, df_n]).reset_index(drop = True)

    elif get_close_matches(movie_dict['name'], df.title.tolist(), cutoff = .7):
        movie_dict['name'] = get_close_matches(movie_dict['name'], df.title.tolist(), cutoff = .7)[0]
    
    else:
        movie_dict = getMovie(movie_dict['name'])
        df_n = pd.DataFrame(
            movie_dict,
            columns = ['title', 'rating', 'feature'],
            index = [0]
        )
   
        df = pd.concat([df, df_n]).reset_index(drop = True)

    # We have a valid target. Now to create a recommendation list.
    # Initialize TFIDF Vectorizer.
    v = TfidfVectorizer()

    # Vectorize the 'feature' column.
    tfidf_matrix = v.fit_transform(df.feature)

    # Create a cosine similarity matrix of the TFIDF matrix.
    cos_sim = cosine_similarity(tfidf_matrix)

    # Get the index of the target movie.
    movie_id = df.loc[df['title'] == movie_dict['name'], :].index[0]

    # Get a list of the cosine similarity scores for target movie.
    score = list(enumerate(cos_sim[movie_id]))

    # Sort that list of similarities.
    sorted_score = sorted(score, key = lambda x: x[1], reverse = True)

    # Return the information for use with the site.
    # Response will be structured as:
    # results = 
    # {
    #     "target": 
    #     {
    #         "title": ...,
    #         "rating": ...
    #     },
    #     "results": 
    #     [
    #         {
    #             "title": ...,
    #             "rating": ...
    #         },
    #         {
    #             "title": ...,
    #             "rating": ...
    #         },
    #         ...
    #     ]
    # }

    results = dict()
    results['results'] = list()

    for i, item in enumerate(sorted_score[0:list_length + 2]):
        result = dict()

        # Separate the target movie.
        if i == 1:
            result['title'] = df.loc[item[0], 'title']
            result['rating'] = df.loc[item[0], 'rating']
            results['target'] = result
        
        # Add remainder to the results list.
        else:
            result['title'] = df.loc[item[0], 'title']
            result['rating'] = df.loc[item[0], 'rating']
            results['results'].append(result)

    return results