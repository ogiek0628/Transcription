from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config.from_pyfile('config.py')
    app.register_blueprint(main)

    return app
