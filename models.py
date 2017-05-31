import datetime, re

from app import db, login_manager, bcrypt

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
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
                     
    # Query the Tag model via the entry_tags table.
    # Create a back reference that allows to go from the Tag model back to
    # the list of blog entries.
    # Use lazy='dynamic' to get a Query object.
    tags = db.relationship('Tag', secondary=entry_tags,
                           backref=db.backref('entries', lazy='dynamic'))
    # The comments attribute on any given entry will be a filterable query.
    comments = db.relationship('Comment', backref='entry', lazy='dynamic')
                              
    def __init__(self, *args, **kwargs):
        # Call parent constructor.
        super(Entry, self).__init__(*args, **kwargs)
        # Automatically set the slug based on the title.
        self.generate_slug()
        
    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)
            
    @property
    def tag_list(self):
        """
        Return a string of tags joined by a comma.
        """
        return ', '.join(tag.name for tag in self.tags)
        
    @property
    def tease(self):
        """
        Return the first 100 characters in the body's text.
        """
        return self.body[:100]
            
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
    admin = db.Column(db.Boolean, default=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    entries = db.relationship('Entry', backref='author', lazy='dynamic')    
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.generate_slug()
        
    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)
            
    # Flask-login interface.
    def get_id(self):
        """
        Instruct Flask-login how to determine the id of a user, which
        will then be stored in the session.
        """
        return str(self.id)
        
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return self.active
        
    def is_anonymous(self):
        return False
        
    @staticmethod
    def make_password(plaintext):
        """
        Accept a plaintext password and return the hashed version.
        """
        return bcrypt.generate_password_hash(plaintext)
        
    def check_password(self, raw_password):
        """
        Accept a plaintext password and determine whether it matches
        the hashed version stored in the database.
        """
        return bcrypt.check_password_hash(self.password_hash, raw_password)
        
    @classmethod
    def create(cls, email, password, **kwargs):
        """
        Create a new user and automatically hash the password
        before saving.
        """
        return User(
            email=email,
            password_hash=User.make_password(password),
            **kwargs)
    
    @staticmethod
    def authenticate(email, password):
        """
        Retrieve a user given a username and password.
        """
        user = User.query.filter(User.email == email).first()
        if user and user.check_password(password):
            return user
        return False
        
    def is_admin(self):
        """
        Determine if the given user is an admin.
        """
        return self.admin
        
class Comment(db.Model):
    STATUS_PENDING_MODERATION = 0
    STATUS_PUBLIC = 1
    STATUS_SPAM = 8
    STATUS_DELETED = 9
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    url = db.Column(db.String(100))
    ip_address = db.Column(db.String(64))
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    
    def __repr__(self):
        return '<Comment from {}>'.format(self.name)
            
# Tell Flask-login how to determine which user is logged in.
@login_manager.user_loader
def _user_loader(user_id):
    """
    Accept the id stored in the session and return a User
    object from the database.
    """
    return User.query.get(int(user_id))