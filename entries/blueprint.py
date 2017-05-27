from flask import Blueprint, render_template, request

from helpers import object_list
from models import Entry, Tag

entries = Blueprint('entries', __name__,
                    template_folder='templates')
                    
def entry_list(template, query, **context):
    """
    Filter and return results based on the search inquiry.
    """
    search = request.args.get('q')
    # If 'q' is present, return only the entries that contain the
    # search phrase in either the title or the body.
    if search:
        query = query.filter(
            (Entry.title.contains(search))|
            (Entry.body.contains(search)))
    return object_list(template, query, **context)
                    
@entries.route('/')
def index():
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    # Return a paginated list of entries.
    return object_list('entries/index.html', entries)
    
@entries.route('/tags/')
def tag_index():
    """
    Render all the tags in the database.
    """
    tags = Tag.query.order_by(Tag.name)
    return object_list('entries/tag_index.html', tags)

@entries.route('/tags/<slug>/')
def tag_detail(slug):
    """
    Render the entries matching a given tag.
    """
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.order_by(Entry.created_timestamp.desc())
    return object_list('entries/tag_detail.html', entries, tag=tag)

@entries.route('/<slug>/')
def detail(slug):
    """
    Render the contents of a single blog entry.
    """
    # Return a 404 if none matches.
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    return render_template('entries/detail.html', entry=entry)