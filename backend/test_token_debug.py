"""Debug token creation and validation"""
import requests

BASE_URL = "http://192.168.178.100:8000"

# Login to get token
login_response = requests.post(
    f"{BASE_URL}/api/v1/auth/login",
    data={"username": "testuser1", "password": "SecurePass123!"}
)

print("Login Response:")
print(f"Status: {login_response.status_code}")
print(f"Response: {login_response.json()}")

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"\nToken: {token[:50]}...")

    # Try to get current user
    headers = {"Authorization": f"Bearer {token}"}
    me_response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)

    print(f"\nGet /me Response:")
    print(f"Status: {me_response.status_code}")
    try:
        print(f"Response: {me_response.json()}")
    except:
        print(f"Response: {me_response.text}")

    # Decode token locally to see what's inside
    from jose import jwt
    try:
        # Don't verify to just see contents
        payload = jwt.decode(token, "", options={"verify_signature": False})
        print(f"\nToken Payload (unverified):")
        print(payload)
    except Exception as e:
        print(f"Error decoding: {e}")
