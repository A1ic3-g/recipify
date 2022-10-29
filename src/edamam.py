import requests
import os
import json
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

def get_recipes(query:str, health:str=None, mealType:str=None, time:int=None) -> json:
    """
    Returns recipes given the search arguments as a JSON object

    :param query: The query string used to search for recipes 
    :param health: Health requirements for recipes
    :param mealType: Breakfast/Lunch/Dinner
    :param time: The maximum amount of time to cook the dish (in mins)
    :return: An array of dictionaries for each recipe wrapped in a JSON object
    """

    # Build the query URL
    url = "https://api.edamam.com/api/recipes/v2?type=public&app_id={0}&app_key=%20{1}%09&q={2}".format(os.environ.get("edamam_id"), os.environ.get("edamam_key"), query)
    if health != None: 
        url += "&health=" + health
    if mealType != None:
        url += "&mealType=" + mealType
    if time != None:
        url += "&time=" + str(time)
    url += "&field=label&field=image&&field=healthLabels&field=url&field=calories&&field=totalTime&field=cuisineType&field=mealType&field=dishType"

    # Query the API
    response = requests.get(url).json()['hits']

    # Convert the output into an array
    output = []
    for recipe in response:
        temp = {}
        temp['label'] = recipe['recipe']['label']
        temp['image'] = recipe['recipe']['image']
        temp['healthLabels'] = recipe['recipe']['healthLabels']
        temp['url'] = recipe['recipe']['url']
        temp['calories'] = int(recipe['recipe']['calories'])
        temp['time'] = int(recipe['recipe']['totalTime'])
        temp['cuisines'] = recipe['recipe']['cuisineType']
        temp['mealTypes'] = recipe['recipe']['mealType']
        temp['dishTypes'] = recipe['recipe']['dishType']
        output.append(temp)

    return json.dumps(output) # Wrap the array in a JSON object