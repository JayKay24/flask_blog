from wtforms.fields import SelectField
from wtforms.fields import PasswordField
from flask.ext.admin import Admin
# Flask-Admin contrib package provides out-of-the-box create,
# read, update and delete functionalities in special views designed
# to work with SQLAlchemy models.
from flask.ext.admin.contrib.sqla import ModelView

from app import app, db
from models import Entry, Tag, User

class EntryModelView(ModelView):
    # Display a human-readable value to the status column.
    # Provide a mapping of the status vaue to display the value.
    _status_choices = [(choice, label) for choice, label in [
        (Entry.STATUS_PUBLIC, 'Public'),
        (Entry.STATUS_DRAFT, 'Draft'),
        (Entry.STATUS_DELETED, 'Deleted')    
    ]]

    column_choices = {
        'status': _status_choices,    
    }    
    
    column_filters = [
        'status', User.name, User.email, 'created_timestamp'    
    ]    
    
    column_list = [
        'title', 'status', 'author', 'tease', 'tag_list',
        'created_timestamp'
    ]
    # Textbox to search title and body fields.
    column_searchable_list = ['title', 'body']
    
    column_select_related_list = ['author'] # Efficiently SELECT the author.

    form_args = {
        'status': {'choices': _status_choices, 'coerce': int},    
    }
    form_columns = ['title', 'body', 'status', 'author', 'tags']
    form_overrides = {'status': SelectField}
    # When we are looking up the author, search on the author's name or email.    
    form_ajax_refs = {
        'author': {
            'fields': (User.name, User.email)        
        }    
    }

class UserModelView(ModelView):
    column_list = ['email', 'name', 'active', 'created_timestamp']

    column_filters = [User.active, 'created_timestamp']
    
    column_searchable_list = ['email', 'name']
    form_columns = ['email', 'password', 'name', 'active']
    form_extra_fields = {
        'password': PasswordField('New Password'),    
    }
    
    def on_model_change(self, form, model, is_created):
        """
        Enter a new password, replacing the old one.
        """
        if form.password.data:
            model.password_hash = User.make_password(form.password.data)
        return super().on_model_change(form, model, is_created)
# To avoid a circular import, admin is loaded after app.
admin = Admin(app, 'Blog Admin')
# Call admin.admin_view and pass instances of the ModelView class
# as well as the db session, for it to access the database with.
admin.add_view(EntryModelView(Entry, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(UserModelView(User, db.session))