import os
class Configuration:
    # Provide the path to the database file.
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG=True
    SECRET_KEY = 'savitar&zoom'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/blog.db'.format(APPLICATION_DIR)
    STATIC_DIR = os.path.join(APPLICATION_DIR, 'static')
    IMAGES_DIR = os.path.join(STATIC_DIR, 'images')