#!/bin/bash

echo "🧪 Testing ChamaNexus Authentication API Endpoints"
echo "=================================================="

BASE_URL="http://localhost:8000/api/v1/accounts"
EMAIL="testuser@example.com"
PASSWORD="TestPassword123"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ SUCCESS: $2${NC}"
    else
        echo -e "${RED}✗ FAILED: $2${NC}"
    fi
}

echo -e "\n${YELLOW}1. Testing Health Check${NC}"
curl -s -X GET "$BASE_URL/health/" | jq . 2>/dev/null || curl -s -X GET "$BASE_URL/health/"
echo ""

echo -e "\n${YELLOW}2. Testing User Registration${NC}"
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register/" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "'"$EMAIL"'",
        "first_name": "Test",
        "last_name": "User",
        "password": "'"$PASSWORD"'",
        "password_confirm": "'"$PASSWORD"'",
        "phone_number": "+254712345678"
    }')

echo "$REGISTER_RESPONSE" | jq . 2>/dev/null || echo "$REGISTER_RESPONSE"

# Extract token from registration response
TOKEN=$(echo "$REGISTER_RESPONSE" | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo -e "\n${YELLOW}3. Testing User Login${NC}"
    LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login/" \
        -H "Content-Type: application/json" \
        -d '{
            "email": "'"$EMAIL"'",
            "password": "'"$PASSWORD"'"
        }')
    
    echo "$LOGIN_RESPONSE" | jq . 2>/dev/null || echo "$LOGIN_RESPONSE"
    TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"token":"[^"]*' | cut -d'"' -f4)
fi

if [ ! -z "$TOKEN" ]; then
    echo -e "\n${YELLOW}4. Testing Get User Profile${NC}"
    curl -s -X GET "$BASE_URL/users/profile/" \
        -H "Authorization: Token $TOKEN" | jq . 2>/dev/null || curl -s -X GET "$BASE_URL/users/profile/" -H "Authorization: Token $TOKEN"
    
    echo -e "\n${YELLOW}5. Testing Change Password${NC}"
    curl -s -X PUT "$BASE_URL/users/change-password/" \
        -H "Authorization: Token $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "old_password": "'"$PASSWORD"'",
            "new_password": "NewPassword123",
            "confirm_password": "NewPassword123"
        }' | jq . 2>/dev/null || curl -s -X PUT "$BASE_URL/users/change-password/" -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" -d '{"old_password": "'"$PASSWORD"'", "new_password": "NewPassword123", "confirm_password": "NewPassword123"}'
    
    echo -e "\n${YELLOW}6. Testing Logout${NC}"
    curl -s -X POST "$BASE_URL/auth/logout/" \
        -H "Authorization: Token $TOKEN" | jq . 2>/dev/null || curl -s -X POST "$BASE_URL/auth/logout/" -H "Authorization: Token $TOKEN"
else
    echo -e "\n${RED}✗ Cannot get authentication token. Skipping protected endpoints.${NC}"
fi

echo -e "\n${YELLOW}7. Testing Password Reset Request${NC}"
curl -s -X POST "$BASE_URL/password-reset/" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "'"$EMAIL"'"
    }' | jq . 2>/dev/null || curl -s -X POST "$BASE_URL/password-reset/" -H "Content-Type: application/json" -d '{"email": "'"$EMAIL"'"}'

echo -e "\n${YELLOW}🎉 API Testing Complete!${NC}"
