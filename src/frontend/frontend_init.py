from flask import Flask, render_template
from flask_bootstrap import Bootstrap

def create_app():
    """function to create the flask app object"""
    app = Flask(__name__)
    Bootstrap(app)
    
    return app 

app = create_app()

if __name__ == '__main__':
    app.run()

