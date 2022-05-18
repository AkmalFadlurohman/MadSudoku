# app/__init__.py: Flask application instance
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_login import LoginManager
#from flask_restx import Api, Resource

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
app.secret_key = "key1"
app.config['SESSION_TYPE'] = 'filesystem'
#api = Api(app)

from app import routes, models
