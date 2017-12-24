from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_login import LoginManager

app = Flask(__name__) #Defines Python flask application
app.config.from_object(Config) #Configures database
db = SQLAlchemy(app) #Database from SQLAlchemy
migrate = Migrate(app, db) #Handles database migrations w/ Alembic
login = LoginManager(app) #Login with login manager
login.login_view = 'login' #Protects and mandates login

from app import routes, models