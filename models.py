import datetime, re

from app import db

# Helper function to generate nice-looking URLs.
def slugify(s):
    # Turn a human readable string into a URL separated
    # by hyphens.
    return re.sub('[^\w]+', '-', s).lower()
    
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now,
                                   onupdate=datetime.datetime.now)
                                   
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
        super(self, Tag).__init__(*args, **kwargs)
        self.slug = slugify(self.name)
        
    def __repr__(self):
        return '<Tag: {}>'.format(self.name)