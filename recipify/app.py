from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from src.edamam import get_recipes
import json

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['POST'])
def index_post():
    query = json.loads(get_recipes(request.form['query']))
    #return "<h1>{0}</h1>".format(query)
    return render_template("results.html", image=query[0]['image'], url=query[0]['url'],
        label=query[0]['label'], mealType=query[0]['mealType'][0], cuisine=query[0]['cuisineType'][0],
        calories=query[0]['calories'])

@app.route('/')
def index_page():
    return render_template("home.html")

if __name__ == '__main__':
    
    app.run()