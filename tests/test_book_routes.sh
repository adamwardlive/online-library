#!/bin/bash

# Define the output file
output_file="book_route_test_results.txt"

# Prompt the user for a specific book ID to test.
read -p "Enter the book ID to test (Caution: Book will be deleted): " book_id

# Test GET /books (List all books)
echo "Testing GET /books..." > "$output_file"
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
     -d '{"title":"New Title", "author":"New Author", "genre":["NewGenre1", "NewGenre2", "NewGenre3"], "cover_image":"https://newimage.url/image.jpg"}')
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Test GET /books/{book_id} (Get a single book by ID after update)
echo "Testing GET /books/${book_id} after update..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/books/${book_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Test DELETE /books/{book_id} (Delete a book by ID)
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





