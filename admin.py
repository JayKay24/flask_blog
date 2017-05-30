from flask.ext.admin import Admin
from app import app

# To avoid a circular import, admin is loaded after app.
admin = Admin(app, 'Blog Admin')