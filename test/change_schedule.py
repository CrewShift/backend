import json
import requests
import copy
import random
from datetime import datetime, timedelta


def add_time_offset(time_str: str, offset_minutes: int) -> str:
    """
    Given a time string in "HH:MM" format, adds offset_minutes (can be negative)
    and returns the new time string.
    """
    from datetime import datetime, timedelta
    time_obj = datetime.strptime(time_str, "%H:%M")
    new_time = (time_obj + timedelta(minutes=offset_minutes)).time()
    return new_time.strftime("%H:%M")


def update_schedule_for_test_user():
    # Test user id.
    # user_id = "6M7nQsnYefOHfnDQI94iWJUsUz53"
    user_id = "L9QR1RX0gwZCBIubtElLU81aUkj1"
    # user_id = "hW1M3oKAxOPPKZfUxypq4nsD9HI3" # old test

    # Load the full JSON data from the JSON file.
    with open("example-schedule.json", "r") as f:
        full_data = json.load(f)

    # Extract the schedule list from the full JSON.
    schedule_data = full_data.get("schedule", [])

    # Deep copy the schedule to modify.
    modified_schedule = copy.deepcopy(schedule_data)

    # Find all flights in the schedule.
    flights = []
    for day in modified_schedule:
        if isinstance(day, dict) and day.get("Flights"):
            for flight in day["Flights"]:
                flights.append((day, flight))

    if not flights:
        print("No flights found in schedule.")
        return

    # Randomly choose one flight to modify.
    # day_entry, flight_entry = random.choice(flights)
    day_entry, flight_entry = flights[0]

    # Decide randomly whether to modify departure, arrival, or both.
    modify_dep = random.choice([True, False])
    modify_arr = random.choice([True, False])
    if not (modify_dep or modify_arr):
        modify_dep = True

    # Generate a random offset between 30 and 120 minutes.
    offset = random.randint(30, 120)
    offset = offset if random.choice([True, False]) else -offset

    if modify_dep and "DepTime" in flight_entry and flight_entry["DepTime"]:
        old_dep = flight_entry["DepTime"]
        new_dep = add_time_offset(old_dep, offset)
        flight_entry["DepTime"] = new_dep
        print(f"Modified flight {flight_entry.get('Duty')} departure time from {old_dep} to {new_dep}")

    # if modify_arr and "ArrivalTime" in flight_entry and flight_entry["ArrivalTime"]:
    #     old_arr = flight_entry["ArrivalTime"]
    #     new_arr = add_time_offset(old_arr, offset)
    #     flight_entry["ArrivalTime"] = new_arr
    #     print(f"Modified flight {flight_entry.get('Duty')} arrival time from {old_arr} to {new_arr}")

    # Update the full data with the modified schedule.
    full_data["schedule"] = modified_schedule

    # Optionally, save the modified JSON locally.
    with open("example-schedule.json", "w") as f:
        json.dump(full_data, f, indent=2)

    # Construct the endpoint URL using the user_id in the path.
    url = f"http://localhost:8000/user/{user_id}/schedule"

    headers = {"Authorization": f"Bearer {user_id}"}

    # Send a POST request with the modified full data.
    response = requests.post(url, json=full_data, headers=headers)

    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json())


if __name__ == "__main__":
    update_schedule_for_test_user()
