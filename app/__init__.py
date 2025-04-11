from flask import Flask
from .routes import main
import os

def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config.from_pyfile('config.py')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    app.register_blueprint(main, url_prefix='/')
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    return app
