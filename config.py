class Config(object):
    SECRET_KEY = 'your-secret-key'
    MONGO_URI = 'mongodb://localhost:27017/library'  # Update with your MongoDB URI
    

class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://127.0.0.1:27017/library'  # Make sure this matches the URI used in Compass
    # Add any other development specific settings

class ProductionConfig(Config):
    # Add production specific settings
    pass  # You can use 'pass' as a placeholder if there's no additional setting

