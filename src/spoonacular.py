import requests
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

# Spoonacular API URL
spoonacular_api:str = "https://api.spoonacular.com/"

# Spoonacular API key to start the query
query_start:str = "?apiKey=" + os.environ.get('spoonacular_api')

# List of cuisines supported by Spoonacular
supported_cuisines:List[str] = ["African","American","British",
    "Cajun","Caribbean","Chinese","Eastern European","European",
    "French","German","Greek","Indian","Irish","Italian","Japanese",
    "Jewish","Korean","Latin American","Mediterranean","Mexican",
    "Middle Eastern","Nordic","Southern","Spanish","Thai",
    "Vietnamese"]

def test() -> None:
    """Test the spoonacular API with a basic request"""

    url:str = spoonacular_api
    url += "recipes/complexSearch?"
    url += query_start
    url += "&cuisine=italian"
    print(url)
    response = requests.get(url)
    print(response.json())

def get_recipe_information(id:int, includeNutrition:bool) -> dict:
    """
    Returns a recipe's information as a json

    :param id: The id of the recipe
    :param includeNutrition: If you want nutritional information
    :return: A json of the recipe's information
    """

    url:str = spoonacular_api
    url += "recipes/"
    url += str(id) + "/"
    url += "information"
    url += query_start
    url += "&includeNutrition="
    if includeNutrition:
        url += "true"
    else:
        url += "false"

    print("Querying the spoonacular API with the URL: " + url)

    response = requests.get(url)
    return response.json()

def get_recipe_cuisines(id:int) -> List[str]:
    """
    Returns the cuisines of the recipie with the provided id

    :param id: The id of the recipe
    :return: The cuisine of the recipe as a list of strings
    """

    response = get_recipe_information(id, False)
    return response['cuisines']

# get_recipe_cuisines(715769)