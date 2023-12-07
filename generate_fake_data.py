# generate_fake_data.py
from faker import Faker
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import random
from datetime import datetime, timedelta
from bson.objectid import ObjectId

fake = Faker()

# Establish a connection to your MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['library']  # Replace 'library' with your database name

# Define the number of items you want to generate
number_of_books = 100
number_of_users = 50
number_of_reviews = 200  # Define how many reviews you want to generate
number_of_borrowed_books = 150

# Generate and insert fake books
book_ids = []
for _ in range(number_of_books):
    book = {
        "title": fake.catch_phrase(),
        "author": fake.name(),
        "genre": [fake.word().capitalize() for _ in range(3)],  # Generates 3 random genres
        "cover_image": fake.image_url(),
    }
    result = db.books.insert_one(book)
    book_ids.append(result.inserted_id)

# Generate and insert fake users
user_ids = []
for _ in range(number_of_users):
    user = {
        "username": fake.user_name(),
        "email": fake.email(),
        "hashed_password": generate_password_hash(fake.password(length=12)),
        "role": 'user' if fake.boolean(chance_of_getting_true=95) else 'admin',  # 5% chance to be admin
    }
    result = db.users.insert_one(user)
    user_ids.append(result.inserted_id)

# Generate and insert fake reviews
for _ in range(number_of_reviews):
    review = {
        "book_id": random.choice(book_ids),
        "user_id": random.choice(user_ids),
        "content": fake.text(),
        "rating": random.randint(1, 5),  # Generates a rating between 1 and 5
    }
    db.reviews.insert_one(review)

for _ in range(number_of_borrowed_books):
    borrowed_date = fake.date_time_between(start_date='-30d', end_date='now')
    due_date = borrowed_date + timedelta(days=14)  # Assuming a two-week loan period
    
    try:
        borrowed_book = {
            "book_id": ObjectId(random.choice(book_ids)),
            "user_id": ObjectId(random.choice(user_ids)),
            "due_date": due_date,
            "returned": fake.boolean(chance_of_getting_true=50),  # 50% chance of the book being returned
            "borrowed_date": borrowed_date,
        }
        db.borrowed_books.insert_one(borrowed_book)
    except Exception as e:
        print(f"An error occurred: {e}")
        break  # Stop the loop if there's an error


print(f"{number_of_books} fake books inserted into the database.")
print(f"{number_of_users} fake users inserted into the database.")
print(f"{number_of_reviews} fake reviews inserted into the database.")
print(f"{number_of_borrowed_books} fake borrowed books inserted into the database.")


