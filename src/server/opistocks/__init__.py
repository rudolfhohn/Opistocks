# Import flask and template operators
from flask import Flask
from flask_cors import CORS, cross_origin

# Define the WSGI application object
app = Flask(__name__, instance_relative_config=True)

CORS(app)

# Configurations
app.config.from_object('config')
app.config.from_pyfile('config.py')

# Import the views (routes)
import opistocks.views

