from flask import Blueprint, flash, render_template, request, redirect, url_for

from helpers import object_list
from models import Entry, Tag
from entries.forms import EntryForm
from app import db

entries = Blueprint('entries', __name__,
                    template_folder='templates')
                    
def entry_list(template, query, **context):
    """
    Filter and return results based on the search inquiry.
    """
    valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)
    query = query.filter(Entry.status.in_(valid_statuses))
    if request.args.get('q'):
        search = request.args.get('q')
        # If 'q' is present, return only the entries that contain the
        # search phrase in either the title or the body.
        query = query.filter(
            (Entry.title.contains(search))|
            (Entry.body.contains(search)))
    return object_list(template, query, **context)
  
def get_entry_or_404(slug):
    valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)
    query = Entry.query.filter(
        (Entry.slug == slug) &
        (Entry.status.in_(valid_statuses))
    )
    return query.first_or_404()
                  
@entries.route('/')
def index():
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    # Return a paginated list of entries.
    return entry_list('entries/index.html', entries)
    
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
    return entry_list('entries/tag_detail.html', entries, tag=tag)

# This view accepts both GET and POST requests.
# Will get rid of the Method Not Allowed error when form is submitted.
@entries.route('/create/', methods=['GET', 'POST'])
def create():
    """
    Render the form used to create blog entries.
    """
    # Check the request method used.
    if request.method == 'POST':
        # Instanstiate the form and pass in the raw form data.
        form = EntryForm(request.form)
        # Check if the form is valid.
        if form.validate():
            entry = form.save_entry(Entry())
            db.session.add(entry)
            db.session.commit()
            flash('Entry "{}" created successfully.'.format(entry.title), 
                  'success')
            # Redirect to the detail page of the newly-created blog post.
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:
        # Simply display an HTML page containing the form.
        form = EntryForm()
    return render_template('entries/create.html', form=form)

@entries.route('/<slug>/')
def detail(slug):
    """
    Render the contents of a single blog entry.
    """
    # Return a 404 if none matches.
    entry = get_entry_or_404(slug)
    return render_template('entries/detail.html', entry=entry)
    
@entries.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
    entry = get_entry_or_404(slug)
    # Check the request method used.
    if request.method == 'POST':
        # When WTForms receives an obj parameter, it will attempt to 
        # pre-populate the form fields with values taken from obj.
        form = EntryForm(request.form, obj=entry)
        if form.validate():
            entry = form.save_entry(entry)
            db.session.add(entry)
            db.session.commit()
            flash('Entry "{}" has been saved.'.format(entry.title), 
                  'success')
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:
        form = EntryForm(obj=entry)
    # Pass the entry under editing to the template context to display
    # the entry title to the user.
    return render_template('entries/edit.html', entry=entry, form=form)
    
@entries.route('/<slug>/delete/', methods=['GET', 'POST'])
def delete(slug):
    entry = get_entry_or_404(slug)
    if request.method == 'POST':
        # Change the entry status to STATUS_DELETED.
        entry.status = Entry.STATUS_DELETED
        db.session.add(entry)
        db.session.commit()
        flash('Entry "{}" has been deleted.'.format(entry.title), 
              'success')
        return redirect(url_for('entries.index'))
    return render_template('entries/delete.html', entry=entry)