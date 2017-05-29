import datetime, re

from app import db, login_manager

@login_manager.user_loader
def _user_loader(user_id):
    """
    Accept the id stored in the session and return a User
    object from the database.
    """
    return User.query.get(int(user_id))

# Helper function to generate nice-looking URLs.
def slugify(s):
    # Turn a human readable string into a URL separated
    # by hyphens.
    return re.sub('[^\w]+', '-', s).lower()
    
# Specify a table to store the mapping of the pivot table exhibiting the
# many to many relationship between the Entry and Tag models.
entry_tags = db.Table('entry_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))                      
                      )
    
class Entry(db.Model):
    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1
    STATUS_DELETED = 2
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now,
                                   onupdate=datetime.datetime.now)
                     
    # Query the Tag model via the entry_tags table.
    # Create a back reference that allows to go from the Tag model back to
    # the list of blog entries.
    # Use lazy='dynamic' to get a Query object.
    tags = db.relationship('Tag', secondary=entry_tags,
                           backref=db.backref('entries', lazy='dynamic'))
                                   
    def __init__(self, *args, **kwargs):
        # Call parent constructor.
        super(Entry, self).__init__(*args, **kwargs)
        # Automatically set the slug based on the title.
        self.generate_slug()
        
    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)
            
    # Generate a helpful representation of instances of this Entry class.
    def __repr__(self):
        return '<Entry: {}>'.format(self.title)
        
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    
    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)
        
    def __repr__(self):
        return '<Tag: {}>'.format(self.name)
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    active = db.Column(db.Boolean, default=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.generate_slug()
        
    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)