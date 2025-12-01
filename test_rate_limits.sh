#!/bin/bash

echo "🧪 Testing Rate Limiting"
echo "========================"

BASE_URL="http://localhost:8000/api/v1/accounts"

# Function to make request and handle response safely
make_request() {
    local url=$1
    local data=$2
    local response
    response=$(curl -s -w "\n%{http_code}" -X POST "$url" \
      -H "Content-Type: application/json" \
      -d "$data")
    
    local body
    local status_code
    body=$(echo "$response" | head -n -1)
    status_code=$(echo "$response" | tail -n 1)
    
    if [ "$status_code" -eq 000 ]; then
        echo "Server not running or connection refused"
        return 1
    fi
    
    echo "HTTP $status_code"
    if [ -n "$body" ]; then
        echo "$body" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'detail' in data:
        print('Detail:', data['detail'])
    else:
        print('Response:', data)
except json.JSONDecodeError:
    print('Non-JSON response:')
    sys.stdout.write(sys.stdin.read())
except Exception as e:
    print(f'Error parsing response: {e}')
"
    fi
}

echo -e "\n1. Testing Login Rate Limiting (5 attempts per hour)"
for i in {1..6}; do
    echo "Attempt $i:"
    make_request "$BASE_URL/auth/login/" '{
        "email": "test@example.com",
        "password": "wrongpassword"
    }'
    echo
    sleep 1
done

echo -e "\n2. Testing Registration Rate Limiting (3 attempts per hour)"
for i in {1..4}; do
    echo "Attempt $i:"
    make_request "$BASE_URL/auth/register/" "{
        \"email\": \"testuser$i@example.com\",
        \"first_name\": \"Test\",
        \"last_name\": \"User\",
        \"password\": \"password123\",
        \"password_confirm\": \"password123\"
    }"
    echo
    sleep 1
done

echo -e "\n🎉 Rate Limit Testing Complete!"
