from flask import Flask # Import the Flask class from the flask module
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Create an instance of Flask called app which will be the central object
app = Flask(__name__)
# Set the configuration for the app
app.config.from_object(Config)

# Create an instance of SQLAlchemy called db which be the cental object for our database
db = SQLAlchemy(app)
# Create an instance of Migrate with the app and db
migrate = Migrate(app, db)

# import the routes to the app and also the models
from . import routes, models
