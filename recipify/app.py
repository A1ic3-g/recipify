import json
import random
import src.spotify as spotify
from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from src.edamam import get_recipes

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index_page():
    return render_template("home.html")

@app.route('/results', methods=['POST'])
def results_page():
    health = []

    # Add health requirements to health
    if 'vegan' in request.form:
        health.append('vegan')
    if 'vegatarian' in request.form:
        health.append('vegatarian')
    if 'wheat-free' in request.form:
        health.append('wheat-free')
    if 'gluten-free' in request.form:
        health.append('gluten-free')
    if 'dairy-free' in request.form:
        health.append('dairy-free')
    if 'kosher' in request.form:
        health.append('kosher')

    mealType = []

    # Add meal requirements to mealType
    if 'Breakfast' in request.form:
        mealType.append('Breakfast')
    if 'Lunch' in request.form:
        mealType.append('Lunch')
    if 'Dinner' in request.form:
        mealType.append('Dinner')


    # Query the recipes API for recipes that fufill the requirements
    query = json.loads(get_recipes(request.form['query'], health, mealType))

    #return "<h1>{0}</h1>".format(query)
    #return render_template("results.html", image=query[0]['image'], url=query[0]['url'],
    #    label=query[0]['label'], mealType=query[0]['mealType'][0], cuisineType=query[0]['cuisineType'][0],
    #    calories=query[0]['calories'])

    elements = "" # Stores the recipe elements

    # For each returned recipe generate an element
    for i in range(0,len(query)):
        elements += '''<div class="container justify-content-center d-flex" style="padding: 3%">
            <div class="card border-primary mb-3" style="width: 75%;">
                <a href="/recipe?label={label}&url={url}&cuisineType={cuisineType}&mealType={mealType}"><div class="card-body">
                    <div class="row">
                        <div class="col-sm">
                            <img src="{image}" width="100%" height="100%" alt="{label}" style="border-radius: 50%;"/>
                        </div>
                        <div class="col-sm">
                            <div class="coll card text-white bg-primary mb-3" style="height: 100%">
                                <div class="card-header"><h1 style="font-size: 5em">{label}</h1></div>
                                    <div class="card-body">
                                        <h4 class="card-title" style="font-size: 4em">meal: {mealType}</h4>
                                        <h4 class="card-title" style="font-size: 4em">cuisine: {cuisineType}</h4>
                                </div>
                            </div>
                        </div>
                    </div>
                </div></a>
            </div>
        </div> '''.format(url=query[i]['url'], cuisineType=query[i]['cuisineType'][0],
            mealType=query[i]['mealType'][0], image=query[i]['image'], label=query[i]['label'])  # Add the correct details in the correct location

    return render_template("results.html", elements=elements) # Render all the elements

@app.route("/recipe")
def recipe_page():
    # Retrieve recipe from URL and place in recipe dictionary
    label=request.args.get("label")
    url = request.args.get("url")
    cuisineType = request.args.get("cuisineType")
    mealType = request.args.get("mealType")
    recipe = {
        "label":label,
        "url":url,
        "cuisineType": cuisineType,
        "mealType": mealType
    }

    # Retrieve Spotify recommendations for recipe
    playlists = spotify.recommend(recipe)
    print(playlists)

    return render_template(
        "recipe.html",
        spotify_link=playlists[0], # The best playlist
        #spotify_link="38u384bGcqsSEWtub2XbEF",
        recipe_link=url,
        label=label
    )

if __name__ == '__main__':
    app.run(debug=True)