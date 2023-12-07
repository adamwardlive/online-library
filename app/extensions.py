from flask_pymongo import PyMongo

db = PyMongo()

def init_extensions(app):
    db.init_app(app)
    # Initialize other extensions like Flask-Login here

