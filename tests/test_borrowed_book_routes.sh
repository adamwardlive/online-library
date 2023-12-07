#!/bin/bash

# Define the output directory and file
output_dir="test_results"
output_file="$output_dir/test_borrowed_books_routes_results.txt"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Create test instances of book and user
echo "Creating test book and user..." > "$output_file"
book_response=$(curl -s -X POST http://127.0.0.1:5000/books -H "Content-Type: application/json" -d '{"title":"Test Book", "author":"Test Author", "genre":["Fiction"], "cover_image":"https://example.com/cover.jpg"}')
book_id=$(echo "$book_response" | jq -r '.msg' | grep -oE '[0-9a-f]{24}')
user_response=$(curl -s -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d '{"username":"testuser", "email":"testuser@example.com", "password":"testpassword"}')
user_id=$(echo "$user_response" | jq -r '.msg' | grep -oE '[0-9a-f]{24}')
echo "Book ID: $book_id, User ID: $user_id" >> "$output_file"

# Create a test borrowed book
echo "Creating test borrowed book..." >> "$output_file"
borrowed_book_response=$(curl -s -X POST http://127.0.0.1:5000/borrowed_books -H "Content-Type: application/json" -d "{\"book\": \"$book_id\", \"user\": \"$user_id\", \"borrowed_date\": \"2023-01-01\", \"due_date\": \"2023-01-15\"}")
borrowed_book_id=$(echo "$borrowed_book_response" | jq -r '.msg' | grep -oE '[0-9a-f]{24}')
echo "Borrowed Book ID: $borrowed_book_id" >> "$output_file"

# Retrieve and display the borrowed book details
echo "Retrieving borrowed book details..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/borrowed_books/$borrowed_book_id)
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Update the borrowed book and display the updated response
echo "Updating borrowed book data..." >> "$output_file"
update_data='{"returned": true}'
response=$(curl -s -X PUT http://127.0.0.1:5000/borrowed_books/$borrowed_book_id -H "Content-Type: application/json" -d "$update_data")
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Retrieve and display the updated borrowed book details
echo "Retrieving updated borrowed book details..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/borrowed_books/$borrowed_book_id)
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Delete the borrowed book and display the delete response
echo "Deleting the borrowed book..." >> "$output_file"
response=$(curl -s -X DELETE http://127.0.0.1:5000/borrowed_books/$borrowed_book_id)
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Confirm the deletion of the borrowed book
echo "Confirming borrowed book deletion..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/borrowed_books/$borrowed_book_id)
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

echo "Tests completed. Results are in $output_file"
