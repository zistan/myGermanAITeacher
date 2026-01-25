"""Debug grammar practice start endpoint"""
import requests
import json

BASE_URL = "http://192.168.178.100:8000"

# Login first
login_response = requests.post(
    f"{BASE_URL}/api/v1/auth/login",
    data={"username": "testuser1", "password": "SecurePass123!"}
)

print(f"Login Status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Try to start practice session
    practice_data = {
        "topic_ids": [1, 2],
        "exercise_count": 5,
        "difficulty_level": None,
        "exercise_types": None,
        "context_category": None,
        "use_spaced_repetition": False
    }

    print(f"\nSending request: {json.dumps(practice_data, indent=2)}")

    practice_response = requests.post(
        f"{BASE_URL}/api/grammar/practice/start",
        json=practice_data,
        headers=headers
    )

    print(f"\nPractice Start Status: {practice_response.status_code}")
    print(f"Response: {practice_response.text}")

    try:
        data = practice_response.json()
        print(f"\nJSON Response: {json.dumps(data, indent=2)}")
    except:
        print("Could not parse as JSON")
