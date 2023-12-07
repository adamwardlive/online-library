#!/bin/bash

# Define the base URL for your Flask API
base_url="http://127.0.0.1:5000"

# Create a test user
echo "Creating test user..."
user_response=$(curl -s -X POST "$base_url/users" \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser", "email":"testuser@example.com", "password":"testpassword"}')
user_id=$(echo "$user_response" | jq -r '.msg' | grep -oE '[0-9a-f]{24}')

# Create a test book
echo "Creating test book..."
book_response=$(curl -s -X POST "$base_url/books" \
     -H "Content-Type: application/json" \
     -d '{"title":"Test Book", "author":"Test Author", "genre":["Fiction"], "cover_image":"https://example.com/cover.jpg"}')
book_id=$(echo "$book_response" | jq -r '.msg' | grep -oE '[0-9a-f]{24}')

# Create a test review
echo "Creating test review..."
review_response=$(curl -s -X POST "$base_url/reviews" \
     -H "Content-Type: application/json" \
     -d "{\"book_id\": \"$book_id\", \"user_id\": \"$user_id\", \"rating\": 5, \"text\": \"Great book!\"}")

# Create a test borrowed book
echo "Creating test borrowed book..."
borrowed_book_response=$(curl -s -X POST "$base_url/borrowed_books" \
     -H "Content-Type: application/json" \
     -d "{\"book\": \"$book_id\", \"user\": \"$user_id\", \"borrowed_date\": \"2023-01-01\", \"due_date\": \"2023-01-15\"}")

# Display responses
echo "User response: $user_response"
echo "Book response: $book_response"
echo "Review response: $review_response"
echo "Borrowed book response: $borrowed_book_response"


