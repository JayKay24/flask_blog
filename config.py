import os
class Configuration:
    # Provide the path to the database file.
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/blog.db'.format(APPLICATION_DIR)
    