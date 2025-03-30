import os
import asyncio
import base64
import requests
import tempfile
from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from database import db  # Assumes your Firestore client is imported from database.py

router = APIRouter()


@router.get("/schedule")
async def get_schedule():
    # Hardcoded user ID for the purpose of the demo
    user_id = "6M7nQsnYefOHfnDQI94iWJUsUz53"

    # Reference to the schedules subcollection under /user/{user_id}
    schedules_ref = db.collection("user").document(user_id).collection("schedules")

    # Query the latest schedule update by ordering by timestamp descending
    docs = list(schedules_ref.order_by("timestamp", direction="DESCENDING").limit(1).stream())

    if docs:
        # Try to extract the saved schedule data from the "data" field.
        latest_data = docs[0].to_dict().get("data")
        if not latest_data:
            # Fallback: if the "data" field is not found, use the entire document.
            latest_data = docs[0].to_dict()
    else:
        return JSONResponse(content={"error": "No schedule found for user"}, status_code=404)

    # Return the schedule data exactly as it was stored (should include keys "statistics" and "schedule")
    return JSONResponse(content=latest_data)
