"""Quick test to debug grammar topics endpoint"""
import requests

BASE_URL = "http://192.168.178.100:8000"

# Login first
login_response = requests.post(
    f"{BASE_URL}/api/v1/auth/login",
    data={"username": "testuser1", "password": "SecurePass123!"}
)

print(f"Login Status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json()["access_token"]

    # Try to get grammar topics
    headers = {"Authorization": f"Bearer {token}"}
    topics_response = requests.get(f"{BASE_URL}/api/grammar/topics", headers=headers)

    print(f"\nGrammar Topics Status: {topics_response.status_code}")
    print(f"Response: {topics_response.text[:500]}")

    try:
        data = topics_response.json()
        print(f"\nJSON Response: {data}")
    except:
        print("Could not parse as JSON")
