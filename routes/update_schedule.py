import os
import logging
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from firebase_admin import messaging
from database import db, save_to_firestore
from auth import get_current_user, User

router = APIRouter()


def compute_schedule_diff(new_data, old_data):
    """
    Compare the new and old schedule data and return a list of difference messages.
    Both new_data and old_data are expected to be full JSON objects.
    The actual schedule is extracted from the "schedule" key.
    Checks changes in departure/arrival times and missing flights (cancellations).
    """
    # Extract schedule lists.
    new_schedule = new_data.get("schedule", []) if isinstance(new_data, dict) else new_data
    old_schedule = old_data.get("schedule", []) if isinstance(old_data, dict) else old_data

    diffs = []
    # Build maps keyed by Date and Duty for the old schedule.
    old_map = {}
    for day in old_schedule:
        if not isinstance(day, dict):
            continue
        date = day.get("Date")
        if date and "Flights" in day and isinstance(day["Flights"], list):
            flights_map = {}
            for flight in day["Flights"]:
                if isinstance(flight, dict) and flight.get("Duty"):
                    flights_map[flight.get("Duty")] = flight
            old_map[date] = flights_map

    # Build maps for the new schedule.
    new_map = {}
    for day in new_schedule:
        if not isinstance(day, dict):
            continue
        date = day.get("Date")
        if date and "Flights" in day and isinstance(day["Flights"], list):
            flights_map = {}
            for flight in day["Flights"]:
                if isinstance(flight, dict) and flight.get("Duty"):
                    flights_map[flight.get("Duty")] = flight
            new_map[date] = flights_map

    # Check for changes and additions in the new schedule.
    for day in new_schedule:
        if not isinstance(day, dict):
            continue
        date = day.get("Date")
        if not date or "Flights" not in day:
            continue
        flights = day.get("Flights", [])
        if not isinstance(flights, list):
            continue
        for flight in flights:
            if not isinstance(flight, dict):
                continue
            duty = flight.get("Duty")
            if not duty:
                continue
            new_dep = flight.get("DepTime")
            new_arr = flight.get("ArrivalTime")
            if date in old_map and duty in old_map[date]:
                old_flight = old_map[date][duty]
                old_dep = old_flight.get("DepTime")
                old_arr = old_flight.get("ArrivalTime")
                if new_dep != old_dep or new_arr != old_arr:
                    diff_msg = (f"Flight {duty} on {date} changed: "
                                f"DepTime {old_dep} -> {new_dep}, "
                                f"ArrivalTime {old_arr} -> {new_arr}")
                    diffs.append(diff_msg)
                    logging.info("Difference found: " + diff_msg)
            else:
                diff_msg = f"New flight {duty} added on {date}."
                diffs.append(diff_msg)
                logging.info("Difference found: " + diff_msg)

    # Check for cancellations: flights in the old schedule but not in the new schedule.
    for day in old_schedule:
        if not isinstance(day, dict):
            continue
        date = day.get("Date")
        if not date or "Flights" not in day:
            continue
        flights = day.get("Flights", [])
        if not isinstance(flights, list):
            continue
        for flight in flights:
            if not isinstance(flight, dict):
                continue
            duty = flight.get("Duty")
            if not duty:
                continue
            if date in new_map and duty not in new_map[date]:
                diff_msg = f"Flight {duty} on {date} canceled."
                diffs.append(diff_msg)
                logging.info("Difference found: " + diff_msg)
    return diffs


def send_push_notification(fcm_token: str, title: str, body: str):
    """Send push notification via Firebase Cloud Messaging"""
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=fcm_token,
    )
    try:
        response = messaging.send(message)
        logging.info(f"Successfully sent notification: {response}")
        logging.info(f"Notification sent to token: {fcm_token} with title: {title} and body: {body}")
    except Exception as e:
        logging.error(f"Error sending notification: {str(e)}")


@router.post("/user/{user_id}/schedule")
async def update_schedule(user_id: str, request: Request, current_user: User = Depends(get_current_user)):
    logging.info(f"URL user_id: {user_id}, current_user.uid: {current_user.uid}")

    if current_user.uid != user_id:
        logging.error("User ID mismatch: Not authorized to update this schedule")
        raise HTTPException(status_code=403, detail="Not authorized to update this schedule")

    try:
        # Read the full new data (which includes statistics and schedule).
        new_data = await request.json()
        logging.info(f"Received new data: {new_data}")

        # Retrieve the latest schedule update from Firestore.
        user_doc_ref = db.collection("user").document(user_id)
        schedules_ref = user_doc_ref.collection("schedules")
        previous_schedule_docs = list(schedules_ref.order_by("timestamp", direction="DESCENDING").limit(1).stream())

        previous_data = None
        if previous_schedule_docs:
            doc = previous_schedule_docs[0]
            prev_doc = doc.to_dict()
            # Try to get the schedule data from the "data" field; if not present, use the entire document.
            previous_data = prev_doc.get("data") or prev_doc
            logging.info(f"Previous schedule data found with timestamp {prev_doc.get('timestamp')}")
        else:
            logging.info("No previous schedule found; skipping diff check.")

        # If a previous schedule exists, compute the differences.
        if previous_data:
            diffs = compute_schedule_diff(new_data, previous_data)
            if diffs:
                logging.info("Differences detected: " + "; ".join(diffs))
                # Retrieve the user's FCM token from the parent user document.
                user_token_doc = db.collection("user").document(user_id).get()
                if not user_token_doc.exists:
                    logging.info("User document not found in Firestore. Creating an empty user document.")
                    # Create an empty document so that we can store the token later.
                    db.collection("user").document(user_id).set({})
                    user_token_doc = db.collection("user").document(user_id).get()
                if user_token_doc.exists:
                    fcm_token = user_token_doc.to_dict().get("fcm_token")
                    if fcm_token:
                        title = "Schedule Update"
                        body = "\n".join(diffs)
                        send_push_notification(fcm_token, title, body)
                    else:
                        logging.info("No FCM token found for user in the user document.")
                else:
                    logging.info("User token document still does not exist in Firestore.")
            else:
                logging.info("No differences detected in schedule update.")
        else:
            logging.info("No previous schedule data to compare.")

        # Generate a new schedule ID using the current UTC timestamp.
        schedule_id = datetime.utcnow().isoformat() + "Z"
        schedule_doc_ref = schedules_ref.document(schedule_id)
        logging.info("Created schedule document reference with ID: %s", schedule_id)

        # Save the full new data along with the timestamp.
        save_to_firestore(schedule_doc_ref, {"data": new_data, "timestamp": schedule_id})
        logging.info("New schedule update saved to Firestore successfully.")

        return JSONResponse(content={"success": True, "schedule_id": schedule_id})
    except Exception as e:
        logging.exception("Error updating schedule in Firestore:")
        raise HTTPException(status_code=500, detail=str(e))
