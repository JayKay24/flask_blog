from flask import Flask

# Import the configuration data.
from config import Configuration

app = Flask(__name__)
# Use the values from the Configuration object in config.py
app.config.from_object(Configuration)