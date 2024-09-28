# Dependencies.
# Data.
import pandas as pd
import numpy as np

# Pre-processing.
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

# Model.
from sklearn.neighbors import NearestNeighbors

# Misc.
from difflib import *

# Get rid of warnings.
import warnings
warnings.filterwarnings('ignore')

# ---

def recommend(list_length, movie_name, movie_genres):
    # Load the dataset.
    df = pd.read_csv("resources/movie_dataset.csv")

    # Drop the columns that we will not need at all.
    df = df.drop(columns = ["genre", "release_year", "runtime", "rating", "vote_count",
                            "director", "cast1", "cast2", "cast3", "cast4", "overview",
                            "gross", "poster_link", "source"])

    # Define features and metadata.
    meta = ['title']
    features = [
        'Action', 
        'Adventure', 
        'Animation',
        'Biography', 
        'Comedy',
        'Crime',
        'Documentary',
        'Drama',
        'Family',
        'Fantasy',
        'Film-Noir',
        'History',
        'Horror',
        'Music',
        'Musical',
        'Mystery',
        'Romance',
        'Sci-Fi',
        'Science Fiction',
        'Sport',
        'Thriller',
        'TV Movie',
        'War',
        'Western'
    ]

    # Omit user's submitted movie from the dataset to avoid showing it as a recommendation.

    movie_titles = df.title.tolist()
    close_match = get_close_matches(movie_name, movie_titles)
    
    if movie_name in movie_titles:
        df.drop(df.loc[df['title'] == movie_name, :].index, inplace = True)

    elif close_match:
        df.drop(df.loc[df['title'] == close_match[0], :].index, inplace = True)

    # Define X.
    X = df.loc[:, features]
    
    # Initialize the KNN Model.
    k = list_length
    model = NearestNeighbors(n_neighbors = k, metric = 'cosine')

    # Fit the Nearest Neighbors model.
    model.fit(X)

    # Get the target features.
    # Note: movie_genres should be a list of 0 or 1 pertaining to the genre columns it belongs to.
    # - OR we could make it a string of genres 'Animation, Drama, Comedy' that can be split into the proper organization.
    # - But I want the list to be used here.

    # movie_genres ...

    # Find the nearest neighbors.
    distances, indices = model.kneighbors(movie_genres)

    # Retrieve the metadata for the results.
    movies = df.iloc[indices[0]]
    movies['distance'] = distances[0]

    # Filter the returned data.
    cols = movies.columns # Note: we could filter the returned data here if needed. Omit some columns.
    movies = movies.loc[:, cols]
    movies = movies.sort_values(by = 'distance')

    # Return the recommendations.
    return movies.to_dict(orient = 'records')