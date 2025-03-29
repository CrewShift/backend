import json
import requests

def update_schedule_for_test_user():
    # Test user id.
    user_id = "hW1M3oKAxOPPKZfUxypq4nsD9HI3"

    # Load schedule data from the JSON file.
    with open("example-schedule.json", "r") as f:
        schedule_data = json.load(f)

    # Construct the endpoint URL using the user_id in the path.
    url = f"http://localhost:8000/user/{user_id}/schedule"

    # Set the Authorization header to our test user id.
    headers = {"Authorization": f"Bearer {user_id}"}

    # Send a POST request with the schedule data as JSON.
    response = requests.post(url, json=schedule_data, headers=headers)

    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    update_schedule_for_test_user()
