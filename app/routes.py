from flask import Blueprint, request, current_app, Response, jsonify
from bson.json_util import dumps, ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import hash_password
from config import Config
from flask import request, Response, current_app
from bson import ObjectId, json_util
from datetime import datetime
from flask_jwt_extended import create_access_token
import jwt
from functools import wraps
from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, create_access_token, get_jwt_identity
import datetime
from .extensions import db  # Assuming db is your PyMongo instance
from .models import User  # Assuming User is your user mode

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/books', methods=['POST'])
def create_book():
    book_data = request.json
    book_collection = current_app.db.books

    # Insert the book and get the inserted ID
    result = book_collection.insert_one(book_data)
    inserted_id = result.inserted_id

    # Return the message with the book ID
    return jsonify({'msg': f'Book created successfully with ID: {str(inserted_id)}'}), 201

@main_blueprint.route('/books', methods=['GET'])
def get_books():
    books = current_app.db.books.find({})
    # Use bson.json_util.dumps to convert the cursor to a JSON string
    books_json = dumps(books)
    return books_json

@main_blueprint.route('/books/<book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):
    book = current_app.db.books.find_one({'_id': ObjectId(book_id)})
    if book:
        return Response(dumps(book), mimetype='application/json')
    else:
        return Response(dumps({'error': 'Book not found'}), status=404, mimetype='application/json')

@main_blueprint.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    book_data = request.json
    result = current_app.db.books.update_one({'_id': ObjectId(book_id)}, {'$set': book_data})
    if result.matched_count:
        return Response(dumps({'msg': 'Book updated successfully'}), mimetype='application/json')
    else:
        return Response(dumps({'error': 'Book not found'}), status=404, mimetype='application/json')

@main_blueprint.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    result = current_app.db.books.delete_one({'_id': ObjectId(book_id)})
    if result.deleted_count:
        return Response(dumps({'msg': 'Book deleted successfully'}), mimetype='application/json')
    else:
        return Response(dumps({'error': 'Book not found'}), status=404, mimetype='application/json')



from pymongo.errors import DuplicateKeyError

@main_blueprint.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = request.json
        user_collection = current_app.db.users
        # Hash the password before storing it
        user_data['hashed_password'] = hash_password(user_data['password'])
        del user_data['password']  # Remove the plaintext password

        # Insert the user and get the inserted ID
        result = user_collection.insert_one(user_data)
        inserted_id = result.inserted_id

        # Return the message with the user ID
        return jsonify({'msg': f'User created successfully with ID: {str(inserted_id)}'}), 201
    except DuplicateKeyError:
        return jsonify({'error': 'Username or email already exists'}), 409


@main_blueprint.route('/users', methods=['GET'])
def get_users():
    users = current_app.db.users.find({})
    users_json = dumps(users)
    return users_json

@main_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user_collection = current_app.db.users
    try:
        # Convert the string ID to an ObjectId
        object_id = ObjectId(user_id)
    except:
        return jsonify({'error': 'Invalid user ID format'}), 400

    user = user_collection.find_one({'_id': object_id})
    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId back to string for JSON response
        del user['hashed_password']  # Don't expose the hashed password
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

@main_blueprint.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_collection = current_app.db.users
    user_data = request.json
    try:
        # Convert the string ID to an ObjectId
        object_id = ObjectId(user_id)
    except:
        return jsonify({'error': 'Invalid user ID format'}), 400
    
    # Update user information here, excluding the password field
    user_data.pop('password', None)  # Do not allow password updates via this route
    result = user_collection.update_one({'_id': object_id}, {'$set': user_data})
    
    if result.matched_count:
        return jsonify({'msg': 'User updated successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

@main_blueprint.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_collection = current_app.db.users
    try:
        # Convert the string ID to an ObjectId
        object_id = ObjectId(user_id)
    except:
        return jsonify({'error': 'Invalid user ID format'}), 400
    
    result = user_collection.delete_one({'_id': object_id})
    
    if result.deleted_count:
        return jsonify({'msg': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404



@main_blueprint.route('/reviews', methods=['POST'])
def create_review():
    review_data = request.json
    review_data['book_id'] = ObjectId(review_data['book_id'])  # Convert to ObjectId
    review_data['user_id'] = ObjectId(review_data['user_id'])  # Convert to ObjectId

    # Insert the review and get the inserted ID
    result = current_app.db.reviews.insert_one(review_data)
    inserted_id = result.inserted_id

    # Return the message with the review ID
    return jsonify({'msg': f'Review created successfully with ID: {str(inserted_id)}'}), 201

@main_blueprint.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = current_app.db.reviews.find({})
    reviews_json = json_util.dumps(reviews)
    return Response(reviews_json, mimetype='application/json')

@main_blueprint.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = current_app.db.reviews.find_one({'_id': ObjectId(review_id)})
    if review:
        return Response(json_util.dumps(review), mimetype='application/json')
    else:
        return Response(json_util.dumps({'error': 'Review not found'}), status=404, mimetype='application/json')

@main_blueprint.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review_data = request.json
    result = current_app.db.reviews.update_one({'_id': ObjectId(review_id)}, {'$set': review_data})
    if result.matched_count:
        return Response(json_util.dumps({'msg': 'Review updated successfully'}), mimetype='application/json')
    else:
        return Response(json_util.dumps({'error': 'Review not found'}), status=404, mimetype='application/json')

@main_blueprint.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    result = current_app.db.reviews.delete_one({'_id': ObjectId(review_id)})
    if result.deleted_count:
        return Response(json_util.dumps({'msg': 'Review deleted successfully'}), mimetype='application/json')
    else:
        return Response(json_util.dumps({'error': 'Review not found'}), status=404, mimetype='application/json')



@main_blueprint.route('/borrowed_books', methods=['POST'])
def create_borrowed_book():
    data = request.get_json()
    data['book'] = ObjectId(data['book'])
    data['user'] = ObjectId(data['user'])
    data['borrowed_date'] = datetime.strptime(data['borrowed_date'], "%Y-%m-%d")
    data['due_date'] = datetime.strptime(data['due_date'], "%Y-%m-%d")

    # Insert the borrowed book and get the inserted ID
    result = current_app.db.borrowed_books.insert_one(data)
    inserted_id = result.inserted_id

    # Return the message with the borrowed book ID
    return jsonify({'msg': f'Borrowed book created successfully with ID: {str(inserted_id)}'}), 201

@main_blueprint.route('/borrowed_books', methods=['GET'])
def get_borrowed_books():
    borrowed_books_cursor = current_app.db.borrowed_books.find()
    borrowed_books_list = list(borrowed_books_cursor)
    return Response(json_util.dumps(borrowed_books_list), mimetype='application/json')

@main_blueprint.route('/borrowed_books/<borrowed_book_id>', methods=['GET'])
def get_borrowed_book(borrowed_book_id):
    borrowed_book = current_app.db.borrowed_books.find_one({'_id': ObjectId(borrowed_book_id)})
    if borrowed_book:
        return Response(json_util.dumps(borrowed_book), mimetype='application/json')
    else:
        return Response(json_util.dumps({'error': 'Borrowed book not found'}), status=404, mimetype='application/json')

@main_blueprint.route('/borrowed_books/<borrowed_book_id>', methods=['PUT'])
def update_borrowed_book(borrowed_book_id):
    data = request.get_json()
    result = current_app.db.borrowed_books.update_one({'_id': ObjectId(borrowed_book_id)}, {'$set': data})
    if result.matched_count:
        return Response(json_util.dumps({'msg': 'Borrowed book updated successfully'}), mimetype='application/json')
    else:
        return Response(json_util.dumps({'error': 'Borrowed book not found'}), status=404, mimetype='application/json')

@main_blueprint.route('/borrowed_books/<borrowed_book_id>', methods=['DELETE'])
def delete_borrowed_book(borrowed_book_id):
    result = current_app.db.borrowed_books.delete_one({'_id': ObjectId(borrowed_book_id)})
    if result.deleted_count:
        return Response(json_util.dumps({'msg': 'Borrowed book deleted successfully'}), mimetype='application/json')
    else:
        return Response(json_util.dumps({'error': 'Borrowed book not found'}), status=404, mimetype='application/json')

@main_blueprint.route('/borrowed_books/unreturned', methods=['GET'])
def get_unreturned_books():
    unreturned_books = current_app.db.borrowed_books.find({"returned": False})
    unreturned_books_json = dumps(unreturned_books)
    return Response(unreturned_books_json, mimetype='application/json')


@main_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Fetch user from the database
    user_collection = current_app.db.users
    user = user_collection.find_one({'username': username})

    # Verify user and password
    if user and check_password_hash(user['hashed_password'], password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401


@main_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200