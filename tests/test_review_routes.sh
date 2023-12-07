#!/bin/bash

# Define the output directory and file
output_dir="test_results"
output_file="$output_dir/test_review_routes_results.txt"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Create a test book and extract the book ID
echo "Creating test book..." > "$output_file"
book_response=$(curl -s -X POST http://127.0.0.1:5000/books \
     -H "Content-Type: application/json" \
     -d '{"title":"Test Book", "author":"Test Author", "genre":["Fiction"], "cover_image":"https://example.com/cover.jpg"}')
book_id=$(echo "$book_response" | jq -r '.msg' | grep -oE '[0-9a-f]{24}')
echo "Book ID: $book_id" >> "$output_file"

# Create a test user and extract the user ID
echo "Creating test user..." >> "$output_file"
user_response=$(curl -s -X POST http://127.0.0.1:5000/users \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser", "email":"testuser@example.com", "password":"testpassword"}')
user_id=$(echo "$user_response" | jq -r '.msg' | grep -oE '[0-9a-f]{24}')
echo "User ID: $user_id" >> "$output_file"

# Create a test review using the test book and user IDs
echo "Creating test review..." >> "$output_file"
review_response=$(curl -s -X POST http://127.0.0.1:5000/reviews \
     -H "Content-Type: application/json" \
     -d "{\"book_id\": \"$book_id\", \"user_id\": \"$user_id\", \"rating\": 5, \"text\": \"Great book!\"}")
review_id=$(echo "$review_response" | jq -r '.msg' | grep -oE '[0-9a-f]{24}')
echo "Review ID: $review_id" >> "$output_file"

# Retrieve and display the created review details
echo "Retrieving created review details..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/reviews/${review_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Update the review and display the updated response
echo "Updating the review with 'Updated' data..." >> "$output_file"
response=$(curl -s -X PUT http://127.0.0.1:5000/reviews/${review_id} \
     -H "Content-Type: application/json" \
     -d "{\"rating\": 4, \"text\": \"Updated review text\"}")
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Retrieve and display the updated review details
echo "Retrieving updated review details..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/reviews/${review_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Delete the review and display the delete response
echo "Deleting the review..." >> "$output_file"
response=$(curl -s -X DELETE http://127.0.0.1:5000/reviews/${review_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Attempt to retrieve the deleted review details and display the response
echo "Confirming review deletion..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/reviews/${review_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

echo "Tests completed. Results are in $output_file"
