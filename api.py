from app import api
from models import Comment

# Populate my app with additional URL routes and view code
# that together, consitutes a RESTFUL API.
api.create_api(Comment, methods=['GET', 'POST'])