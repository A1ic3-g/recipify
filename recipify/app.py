from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from src.edamam import get_recipes
import json

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['POST'])
def index_post():
    query = json.loads(get_recipes(request.form['query']))
    return "<h1>{0}</h1>".format(query)

@app.route('/')
def index_page():
    return render_template("home.html")

if __name__ == '__main__':
    
    app.run()