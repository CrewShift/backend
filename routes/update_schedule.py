import os
import logging
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from database import db, save_to_firestore
from auth import get_current_user, User

router = APIRouter()

@router.post("/user/{user_id}/schedule")
async def update_schedule(user_id: str, request: Request, current_user: User = Depends(get_current_user)):
    logging.info(f"URL user_id: {user_id}, current_user.uid: {current_user.uid}")

    if current_user.uid != user_id:
        logging.error("User ID mismatch: Not authorized to update this schedule")
        raise HTTPException(status_code=403, detail="Not authorized to update this schedule")

    try:
        # Read the schedule data from the request body.
        schedule_data = await request.json()
        logging.info(f"Received schedule data: {schedule_data}")

        # Generate a scheduleId using the current UTC timestamp.
        schedule_id = datetime.utcnow().isoformat() + "Z"

        # Get a reference to the user's document.
        user_doc_ref = db.collection("user").document(user_id)

        # Create a new document in the 'schedules' subcollection with the timestamp as its ID.
        schedule_doc_ref = user_doc_ref.collection("schedules").document(schedule_id)
        logging.info("Created schedule document reference with ID: %s", schedule_id)

        # Save the schedule data along with the timestamp.
        save_to_firestore(schedule_doc_ref, {"schedule": schedule_data, "timestamp": schedule_id})
        logging.info("Schedule history saved to Firestore successfully.")

        return JSONResponse(content={"success": True, "schedule_id": schedule_id})
    except Exception as e:
        logging.exception("Error updating schedule in Firestore:")
        raise HTTPException(status_code=500, detail=str(e))
