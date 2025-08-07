import dotenv
import fuzzysearch
import os
import random
from typing import *
import itertools
import base64
import requests
from datetime import datetime, timedelta
from flask import current_app

dotenv.load_dotenv()

# Environment variables
SPOTIFY_CLIENT_KEY: str = "SPOTIFY_CLIENT"
SPOTIFY_SECRET_KEY: str = "SPOTIFY_SECRET"
TOKEN_URL = 'https://accounts.spotify.com/api/token'

_genre_seeds = []

_token_cache = {
    'access_token': None,
    'expires_at': None
}

def get_access_token():
    if _token_cache['access_token'] and datetime.now() < _token_cache['expires_at']:
        return _token_cache['access_token']

    print("Fetching new Spotify access token...")
    client_creds = f"{os.environ.get(SPOTIFY_CLIENT_KEY)}:{os.environ.get(SPOTIFY_SECRET_KEY)}"
    base64_encoded_creds = base64.b64encode(client_creds.encode()).decode()

    headers = {
        'Authorization': f'Basic {base64_encoded_creds}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }

    try:
        response = requests.post(TOKEN_URL, headers=headers, data=data)
        if response.status_code != 200:
            current_app.logger.error(f"Failed to fetch access token: {response.status_code} - {response.text}")
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data.get('access_token')
        expires_in = token_data.get('expires_in', 3600)

        if not access_token:
            raise ValueError("Access token not found in response.")
        
        expires_at = datetime.now() + timedelta(seconds=expires_in) - timedelta(seconds=15)
        
        _token_cache['access_token'] = access_token
        _token_cache['expires_at'] = expires_at
        
        return access_token

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error fetching access token: {e}")
        return None
    except ValueError as e:
        current_app.logger.error(f"Error: {e}")
        return None

def get_recommendation_genres() -> List[str]:
    """
    Retrieve a list of recommendable Spotify genres.

    :return: A list of genres.
    """
    global _genre_seeds
    token = get_access_token()
    
    if not token:
        current_app.logger.error("Failed to retrieve access token. Cannot fetch genres.")
        return []
    
    try:
        # API call to retrieve recommendation genres
        headers = {
            'Authorization': f'Bearer {token}'
        }
        url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        genres = data.get('genres', [])

        if genres:
            _genre_seeds = genres
            current_app.logger.info(f"Retrieved {len(genres)} genres from Spotify.")
        
        return genres
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error fetching recommendation genres: {e}")
        current_app.logger.warning(f"Returning cached genres of length {len(_genre_seeds)}")
        return _genre_seeds
    
def search_playlists(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Searches for playlists on Spotify.

    :param query: The search query string.
    :param limit: The maximum number of results to return (1-50). Defaults to 20.
    :return: A list of dictionaries, where each dictionary represents a playlist.
    """
    token = get_access_token()
    
    if not token:
        current_app.logger.error("Failed to retrieve access token. Cannot search for playlists.")
        return []
        
    if not 1 <= limit <= 50:
        current_app.logger.error("Limit must be between 1 and 50.")
        return []

    url = "https://api.spotify.com/v1/search"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'q': query,
        'type': 'playlist',
        'limit': limit
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        playlists = data.get('playlists', {}).get('items', [])
        
        return playlists
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error searching for playlists: {e}")
        return []

def recommend(recipe: Dict[str, Any]) -> List[Dict]:
    """
    Recommend playlists from Spotify based on a recipe.

    :param recipe: The recipe.
    :return: A list of playlist recommendations.
    """

    current_app
    # List of recommendable Spotify genres
    #genres: List[str] = spotify.recommendation_genre_seeds()["genres"]
    genres = get_recommendation_genres()

    recommendations = []

    # Retrieve playlists matching genres
    cuisines: List[str] = recipe["cuisineType"]
    for cuisine in cuisines:
        for genre in genres:
            fuzzy: List[fuzzysearch.Match] = fuzzysearch.find_near_matches(subsequence=genre, sequence=cuisine, max_l_dist=1)
            match fuzzy:
                case [_]:
                    recommendations.extend(search_playlists(query=genre, limit=1))

    # Retrieve playlists matching main meal type
    meals: List[str] = recipe["mealType"]
    for meal, cuisine in itertools.product(meals, cuisines):
        recommendations.extend(search_playlists(query=f"{cuisine} {meal}", limit=2))

    # If there are no playlists from the genre matching, find playlists based on searching the cuisine and the meal type
    if not recommendations:
        recommendations.extend(search_playlists(query=recipe['label'], limit=1))
        recommendations.extend(search_playlists(query=random.choice(cuisines), limit=1))
        recommendations.extend(search_playlists(query=recipe['mealType'], limit=1))

    # Generic food playlist if absolutely nothing was found
    if not recommendations:
        recommendations.extend(search_playlists(query="food", limit=1))

    return [rec for rec in recommendations if rec is not None]

def get_best_playlist(recommendations:List[Dict]) -> Dict:
    """Returns the best playlist out of a list of recommendations"""

    return recommendations[0]
