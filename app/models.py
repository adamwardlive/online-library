from .extensions import db
from mongoengine import Document, StringField, ReferenceField, IntField, DateTimeField, BooleanField


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    hashed_password = db.StringField(required=True)
    role = db.StringField(required=True, default='user')

class Book(db.Document):
    title = db.StringField(required=True)
    author = db.StringField(required=True)
    genre = db.ListField(db.StringField())
    cover_image = db.StringField()
    availability_status = db.BooleanField(default=True)

class Review(Document):
    book = ReferenceField('Book', required=True)  # Reference to the Book document
    user = ReferenceField('User', required=True)  # Reference to the User document
    content = StringField(required=True)  # The text content of the review
    rating = IntField(min_value=1, max_value=5)  # The rating, for example on a scale from 1 to 5
    created_at = DateTimeField()  # The date and time when the review was created

class BorrowedBook(Document):
    # Assuming each borrowed book record pertains to a specific book and user
    book = ReferenceField('Book', required=True)  # Reference to the Book document
    user = ReferenceField('User', required=True)  # Reference to the User document
    due_date = DateTimeField(required=True)  # The date by which the book should be returned
    returned = BooleanField(default=False)  # Whether the book has been returned
    borrowed_date = DateTimeField()  # The date and time when the book was borrowed

