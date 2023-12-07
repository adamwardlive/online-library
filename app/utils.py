import json
from bson import ObjectId
from werkzeug.security import generate_password_hash

class CustomJSONEncoder(json.JSONEncoder):
    """Extend json-encoder class"""
    def default(self, obj):
        if isinstance(obj, ObjectId):
            # if it's an ObjectId, convert to string
            return str(obj)
        # For other types, use the default encoder
        return json.JSONEncoder.default(self, obj)

def hash_password(password):
    return generate_password_hash(password)