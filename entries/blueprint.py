from flask import Blueprint

from models import Entry, Tag

entries = Blueprint('entries', __name__,
                    template_folder='templates')
                    
@entries.route('/')
def index():
    return 'Entries index'
    
@entries.route('/tags/')
def tag_index():
    pass

@entries.route('/tags/<slug>/')
def tag_detail(slug):
    pass

@entries.route('/<slug>/')
def detail(slug):
    pass