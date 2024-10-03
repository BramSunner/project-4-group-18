# Dependencies.
# Data.
import requests
import pandas as pd

# Misc.
from time import sleep
from itertools import islice
from feature_processor import lemmatizeAssist, processText, columnMerger

# API Access Token
from api_keys import ACCESS_TOKEN

# ----- HELPER FUNCTIONS ----- 

def requestMovie(movie_name):
    '''
    Make a request to The Movie Database API with a given movie name.
    Get the movie ID number from TMDB and then make a second request for more information.
    Returns a dictionary containing movie title, overview, director, and up to 4 cast members.
    If errors occur: a default return of the movie Forrest Gump is given.
    https://www.themoviedb.org
    '''
    default = {
        "title": "Forrest Gump",
        "rating": 8.8,
        "genre": ["Drama", "Romance"],
        "director": "Robert Zemeckis",
        "cast": ["Tom Hanks", "Robin Wright", "Gary Sinise", "Sally Field"],
        "overview": "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate and other historical events unfold through the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart.",
    }

    # Make the first request for the movie ID.
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Request was unsuccessful with code: {response.status_code}")
        return

    else:
        data = response.json()
    
    try:
        movie_id = data.get('results', {})[0].get('id', -1)

    except IndexError as e:
        print("Index does not exist. Returning default.")
        return default
    
    # Make the second request for the needed information.
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=credits&language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    # Make the request.
    sleep(1) # Make sure that we respect the site and limit the speed of our requests.
    response = requests.get(url, headers = headers)

    if response.status_code != 200:
        print(f"Request with code {response.status_code} was unsuccessful. Cancelling...")
        return default

    else:
        data = response.json()

    result = dict()
    result['title'] = data.get('title', '')
    result['rating'] = data.get('rating', 0)
    result['genre'] = [x.get('name', '') for x in data.get('genres', {})]
    result['director'] = next(((x.get('name', '') for x in data.get('credits', {}).get('crew', {}) if x.get('job', '') == 'Director')), '')
    result['cast'] = list(islice((x.get('name', '') for x in data.get('credits', {}).get('cast', {})), 4))
    result['overview'] = data.get('overview', '')

    return result



def getMovie(movie_name):
    # Create DataFrame to run processes on with data from movie request.
    movie_dict = requestMovie(movie_name)

    # Process data to match our DataFrame requirements.
    for i in range(1, 5):
        try:
            movie_dict[f'cast{i}'] = movie_dict['cast'][i-1]

        except KeyError as e:
            movie_dict[f'cast{i}'] = ''
    
    movie_dict['genre'] = ", ".join(movie_dict['genre'])
    movie_dict.pop('cast', None)

    df = pd.DataFrame(
        movie_dict,
        columns = ['title', 'rating', 'genre', 'director', 'cast1', 'cast2', 'cast3', 'cast4', 'overview'],
        index = [0]
    )

    # Run the processing steps on the new data.
    df['genre'] = df.genre.apply(lambda x: x.replace("Sci-Fi", "Science Fiction"))
    df['lemma_text'] = df.overview.apply(lambda x: processText(x))
    df['feature'] = df.apply(lambda row: columnMerger(row), axis = 1)
    df = df[['title', 'rating', 'feature']]

    # Return the new data as a dictionary.
    return df.to_dict(orient = 'records')[0]
