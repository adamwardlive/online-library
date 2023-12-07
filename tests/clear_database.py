from pymongo import MongoClient

# Establish a connection to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['library']  # Replace 'library' with the name of your database

# Clear the 'users' collection
db.users.delete_many({})

# Clear the 'books' collection
db.books.delete_many({})

db.reviews.delete_many({})

db.borrowed_books.delete_many({})

print("All users, books, reviews and borrowed books have been removed from the database.")

