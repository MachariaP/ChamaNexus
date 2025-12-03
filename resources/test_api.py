# test_api.py
import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api/v1'

def test_endpoints():
    # Test health check
    print("Testing health check...")
    response = requests.get(f'{BASE_URL}/health-check/')
    print(f"Health Check: {response.status_code} - {response.json()}")
    
    # Get CSRF token
    print("\nGetting CSRF token...")
    response = requests.get(f'{BASE_URL}/csrf-token/')
    csrf_token = response.json().get('csrfToken')
    print(f"CSRF Token: {csrf_token[:20]}...")
    
    # Test login (use your actual credentials)
    print("\nTesting login...")
    login_data = {
        'email': 'your_email@example.com',
        'password': 'your_password'
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token,
    }
    
    response = requests.post(
        f'{BASE_URL}/accounts/auth/login/',
        json=login_data,
        headers=headers,
        cookies=response.cookies
    )
    
    print(f"Login: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")

if __name__ == '__main__':
    test_endpoints()
