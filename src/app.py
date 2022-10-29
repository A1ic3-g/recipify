from flask import Flask 
from flask_bootstrap import Bootstrap
from frontend import routes

app = Flask(__name__)
Bootstrap(app)

if __name__ == '__main__':
    app.register_blueprint(routes.pages)
    
    app.run()