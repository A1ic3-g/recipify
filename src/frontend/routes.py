from flask import Blueprint, render_template, redirect, url_for, request

pages = Blueprint('pages', __name__)


@pages.route('/')
def index_page():
    return render_template("home.html")


@pages.route('/recipe')
def recipe(): 
    return render_template('recipe.html', recipeName="",
                    cusineType="", 
                    dishType="",
                    spotifyLink="",
                    imageFileLink="",
                    recipeLink="",
    )
    