from flask import request, session

# Import the flask application instance from app.py
from app import app, db

# Import admin after app.
import admin
import api
import models
import views

from entries.blueprint import entries

# Register the blueprint with Flask app object.
# Instruct app object that entries' URLs to live at the prefix /entries.
app.register_blueprint(entries, url_prefix='/entries')

if __name__ == '__main__':
    app.run()