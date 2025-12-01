# test_api.sh
#!/bin/bash

echo "Testing ChamaNexus API endpoints..."

# Test CSRF endpoint
echo -e "\n1. Testing CSRF endpoint..."
curl -X GET "https://chamanexus-backend.onrender.com/api/v1/csrf-token/" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  --cookie-jar cookies.txt \
  --cookie cookies.txt

# Test health endpoint
echo -e "\n2. Testing health endpoint..."
curl -X GET "https://chamanexus-backend.onrender.com/api/v1/accounts/health/" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json"

# Test login endpoint (with dummy data)
echo -e "\n3. Testing login endpoint..."
curl -X POST "https://chamanexus-backend.onrender.com/api/v1/accounts/auth/login/" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}' \
  --cookie-jar cookies.txt \
  --cookie cookies.txt

echo -e "\nTesting complete!"
