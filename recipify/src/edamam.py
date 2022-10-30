import requests
import os
import json
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

def get_recipes(query:str, health:List[str]=None, mealType:List[str]=None) -> json:
    """
    Returns recipes given the search arguments as a JSON object

    :param query: The query string used to search for recipes 
    :param health: List of health requirements for recipes
    :param mealType: List of Breakfast/Lunch/Dinner
    :return: An array of dictionaries for each recipe wrapped in a JSON object
    """

    # Build the query URL
    url = "https://api.edamam.com/api/recipes/v2?type=public&app_id={0}&app_key=%20{1}%09&q={2}".format(os.environ.get("EDAMAM_ID"), os.environ.get("EDAMAM_KEY"), query)

    # Add health requirements
    if health != []: 
        for i in health:
            url += "&health=" + i

    # Add meal requirements
    if mealType != []:
        for i in mealType:
            url += "&mealType=" + i

    # Add return fields
    url += "&field=label&field=image&field=url&field=cuisineType&field=mealType"

    # Query the API
    response = requests.get(url).json()['hits']

    # Convert the output into an array
    output = []
    for recipe in response:
        temp = {}
        temp['label'] = recipe['recipe']['label']
        temp['image'] = recipe['recipe']['image']
        temp['url'] = recipe['recipe']['url']
        temp['cuisineType'] = recipe['recipe']['cuisineType']
        temp['mealType'] = recipe['recipe']['mealType']
        output.append(temp)

    return json.dumps(output) # Wrap the array in a JSON object