from flask.ext.admin import Admin
# Flask-Admin contrib package provides out-of-the-box create,
# read, update and delete functionalities in special views designed
# to work with SQLAlchemy models.
from flask.ext.admin.contrib.sqla import ModelView

from app import app, db
from models import Entry, Tag, User

# To avoid a circular import, admin is loaded after app.
admin = Admin(app, 'Blog Admin')
# Call admin.admin_view and pass instances of the ModelView class
# as well as the db session, for it to access the database with.
admin.add_view(ModelView(Entry, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(User, db.session))