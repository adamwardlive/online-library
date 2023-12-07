#!/bin/bash

# Define the output file
output_file="user_route_test_results.txt"

# Create a test user and get user ID
echo "Creating test user..." > "$output_file"
user_response=$(curl -s -X POST http://127.0.0.1:5000/users \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser", "email":"testuser@example.com", "password":"testpassword"}')
user_id=$(echo "$user_response" | jq -r '.msg' | grep -oE '[0-9a-f]{24}')
echo "User ID: $user_id" >> "$output_file"
echo -e "\n" >> "$output_file"

# Retrieve and display the created user details
echo "Retrieving created user details..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/users/${user_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Update the user's email and display the updated response
echo "Updating the user's email to 'updateduser@example.com'..." >> "$output_file"
response=$(curl -s -X PUT http://127.0.0.1:5000/users/${user_id} \
     -H "Content-Type: application/json" \
     -d '{"email":"updateduser@example.com"}')
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Retrieve and display the updated user details
echo "Retrieving updated user details..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/users/${user_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Delete the user and display the delete response
echo "Deleting the user..." >> "$output_file"
response=$(curl -s -X DELETE http://127.0.0.1:5000/users/${user_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

# Attempt to retrieve the deleted user details and display the response
echo "Confirming user deletion..." >> "$output_file"
response=$(curl -s -X GET http://127.0.0.1:5000/users/${user_id})
echo "$response" | jq '.' >> "$output_file"
echo -e "\n" >> "$output_file"

echo "Tests completed. Results are in $output_file"



