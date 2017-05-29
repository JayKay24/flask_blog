from flask import Flask, g
from flask.ext.login import LoginManager, current_user
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

# Import the configuration data.
from config import Configuration

app = Flask(__name__)

# Use the values from the Configuration object in config.py
app.config.from_object(Configuration)

# Create an object to manage the database connections.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view = "login"

# Signal handler to run before every request.
# Signal handler loads the current user.
@app.before_request
def before_request():
    g.user = current_user