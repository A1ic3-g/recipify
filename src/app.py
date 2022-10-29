
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from frontend import routes

app = Flask(__name__, template_folder="../templates")
Bootstrap(app)

"""
@app.route('/')
def home():
    return render_template('test.html')
"""
if __name__ == '__main__':
    app.register_blueprint(routes.pages)
    
    app.run()