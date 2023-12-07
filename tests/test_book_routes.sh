#!/bin/bash

# Define the output directory and file
output_dir="test_results"
output_file="$output_dir/test_book_routes_results.txt"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Create a test book and get book ID
echo "Creating test book..." > "$output_file"
book_response=$(curl -s -X POST http://127.0.0.1:5000/books \
     -H "Content-Type: application/json" \
     -d '{"title":"Test Book", "author":"Test Author", "genre":["Fiction"], "cover_image":"https://example.com/cover.jpg"}')
book_id=$(echo "$book_response" | jq -r '.msg' | grep -oE '[0-9a-f]{24}')
echo "Book ID: $book_id" >> "$output_file"
echo -e "\n" >> "$output_file"

# Test GET /books (List all books)
echo "Testing GET /books..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/books)
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Test GET /books/{book_id} (Get a single book by ID)
echo "Testing GET /books/${book_id}..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/books/${book_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Test PUT /books/{book_id} (Update a book by ID)
echo "Testing PUT /books/${book_id}..." >> "$output_file"
response=$(curl -s -X PUT http://127.0.0.1:5000/books/${book_id} \
     -H "Content-Type: application/json" \
     -d '{"title":"Updated Title", "author":"Updated Author", "genre":["Updated"], "cover_image":"https://example.com/updated_image.jpg"}')
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Test GET /books/{book_id} (Get the updated book by ID)
echo "Testing GET /books/${book_id} after update..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/books/${book_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Test DELETE /books/{book_id} (Delete the book by ID)
echo "Testing DELETE /books/${book_id}..." >> "$output_file"
response=$(curl -s -X DELETE http://127.0.0.1:5000/books/${book_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Test GET /books/{book_id} (Confirm deletion of the book by ID)
echo "Testing GET /books/${book_id} after delete to confirm deletion..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/books/${book_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

echo "Tests completed. Results are in $output_file"