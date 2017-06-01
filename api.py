from flask.ext.restless import ProcessingException

from app import api
from entries.forms import CommentForm
from models import Comment

def post_preprocessor(data, **kwargs):
    """
    Accept the deserialized POST data as an argument.
    Validate the submitted coment.
    """
    form = CommentForm(data=data)
    if form.validate():
        return form.data
    else:
        # If validation fails, signal to Flask-Restless that this
        # data was unprocessable and return a 400 Bad Request response.
        raise ProcessingException(
            description='Invalid form submission.',
            code=400
        )

# Populate my app with additional URL routes and view code
# that together, consitutes a RESTFUL API.
api.create_api(
    Comment,
    # Restrict the Comment fields returned by the api.
    include_columns=['id', 'name', 'url', 'body', 'created_timestamp'],
    methods=['GET', 'POST'],
    preprocessors={
        'POST': [post_preprocessor],    
    })