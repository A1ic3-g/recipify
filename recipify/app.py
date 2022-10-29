from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from src.edamam import get_recipes
import json
import src.spotify as spotify
import random

app = Flask(__name__)
Bootstrap(app)


@app.route('/', methods=['POST'])
def index_post():
    query = json.loads(get_recipes(request.form['query']))
    return "<h1>{0}</h1>".format(query)


@app.route('/')
def index_page():
    return render_template("home.html")


@app.route("/recipe")
def recipe_page():
    # Retrieve recipe from URL
    name = request.args.get("name")
    cuisines = request.args.get("cuisines").split(',')
    dishes = request.args.get("dishes").split(',')
    meals = request.args.get("meals").split(',')
    recipe = {
        "cuisines": cuisines,
        "meals": meals,
        "dishes": dishes,
        "healths": [],
    }

    # Retrieve Spotify recommendations for recipe
    playlists = spotify.recommend(recipe)
    print(playlists)

    # Render template
    return render_template(
        "recipe.html",
        recipe_name=name,
        recipe_cuisines=cuisines,
        recipe_dishes=dishes,
        spotify_link=random.choice(playlists)["id"],
        recipe_link="",
        image_link="",
    )


if __name__ == '__main__':
    app.run()