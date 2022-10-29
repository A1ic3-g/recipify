
from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index_page():
    return render_template("home.html")

if __name__ == '__main__':
    
    app.run()