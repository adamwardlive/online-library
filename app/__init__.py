from flask import Flask
from pymongo import MongoClient
from .utils import CustomJSONEncoder  # Import your custom encoder
from flask_jwt_extended import JWTManager

def create_app(config_filename='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a strong secret key
    jwt = JWTManager(app)


    # Assign the custom JSON encoder to the Flask app
    app.json_encoder = CustomJSONEncoder

    mongo_client = MongoClient(app.config['MONGO_URI'])
    app.db = mongo_client['library']

    from .routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app

