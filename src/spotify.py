import dotenv
import os
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


def recommend(recipe: Dict[str, Any]) -> Any:
    """
    Recommend a Spotify track based on recipe data.

    :param recipe:
    :return:
    """

    # List of recommendable Spotify genres
    genres: List[str] = spotify.recommendation_genre_seeds()["genres"]

    # Recipe health and dish types
    healths: List[str] = recipe["healthLabels"]
    dishes: List[str] = recipe["dishType"]

    health_genres: List[str] = healths_to_genres(healths, genres)

    return spotify.recommendations(
        seed_genres=genres[:5],
        limit=10,
    )


def healths_to_genres(healths: List[str], genres: List[str]) -> List[str]:
    match healths:
        case ["alcohol-cocktail"]:
            return []


print([track["name"] for track in recommend({})["tracks"]])
