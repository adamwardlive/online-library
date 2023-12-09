from mongoengine import Document, StringField, ReferenceField, IntField, DateTimeField, BooleanField, ListField

class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    hashed_password = StringField(required=True)
    role = StringField(required=True, default='user')

class Book(Document):
    title = StringField(required=True)
    author = StringField(required=True)
    genre = ListField(StringField())
    cover_image = StringField()
    availability_status = BooleanField(default=True)

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

