import dotenv
import fuzzysearch
import os
import random
from spotipy import *
from typing import *

dotenv.load_dotenv()

# Environment variables
SPOTIFY_CLIENT_KEY: str = "SPOTIFY_CLIENT"
SPOTIFY_SECRET_KEY: str = "SPOTIFY_SECRET"

# Connect to the Spotify API
spotify: Spotify = Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=os.getenv(SPOTIFY_CLIENT_KEY),
        client_secret=os.getenv(SPOTIFY_SECRET_KEY),
    ),
)


def recommend(recipe: Dict[str, Any]) -> List[Dict]:
    """
    Recommend playlists from Spotify based on a recipe.

    :param recipe: The recipe.
    :return: A list of playlist recommendations.
    """

    # List of recommendable Spotify genres
    genres: List[str] = spotify.recommendation_genre_seeds()["genres"]

    recommendations = []

    # Retrieve playlists matching genres
    cuisines: List[str] = recipe["cuisineType"]
    for cuisine in cuisines:
        for genre in genres:
            fuzzy: List[fuzzysearch.Match] = fuzzysearch.find_near_matches(subsequence=genre, sequence=cuisine, max_l_dist=1)
            match fuzzy:
                case [_]:
                    recommendations.extend(playlists(query=genre, limit=1))

    # Retrieve playlists matching main meal type
    meals: List[str] = recipe["mealType"]
    match meals:
        case [meal]:
            recommendations.extend(playlists(query=meal, limit=1))

    # If there are no playlists from the genre matching, find playlists based on searching the cuisine and the meal type
    if not recommendations:
        recommendations.extend(playlists(query=recipe['label'], limit=1))
        recommendations.extend(playlists(query=random.choice(cuisines), limit=1))
        recommendations.extend(playlists(query=recipe['mealType'], limit=1))

    # Generic food playlist if absolutely nothing was found
    if not recommendations:
        recommendations.extend(playlists(query="food", limit=1))

    return recommendations


def playlists(query: str, limit: int) -> List[Dict]:
    """
    Retrieve playlists from Spotify based on a query string.

    :param query: The query to use when searching for playlists.
    :param limit: The limit on the number of playlists returned.
    :return: A list of playlists matching the specified query.
    """
    return spotify.search(q=query, type="playlist", limit=limit)["playlists"]["items"]


def get_best_playlist(recommendations:List[Dict]) -> Dict:
    """Returns the best playlist out of a list of recommendations"""

    return recommendations[0]
