from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Import the configuration data.
from config import Configuration

app = Flask(__name__)

# Use the values from the Configuration object in config.py
app.config.from_object(Configuration)

# Create an object to manage the database connections.
db = SQLAlchemy(app)