import os
import logging
from collections import OrderedDict
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from database import db  # Firestore client from your database module

router = APIRouter()


def reassemble_flight(flight: dict) -> OrderedDict:
    """
    Reassemble an individual flight using an OrderedDict with keys in the desired order.
    Desired order:
      "Duty", "CheckIn", "CheckOut", "Departure", "Arrival",
      "DepTime", "ArrivalTime", "Aircraft", "Cockpit", "Cabin"
    """
    ordered_flight = OrderedDict()
    ordered_flight["Duty"] = flight.get("Duty")
    ordered_flight["CheckIn"] = flight.get("CheckIn")
    ordered_flight["CheckOut"] = flight.get("CheckOut")
    ordered_flight["Departure"] = flight.get("Departure")
    ordered_flight["Arrival"] = flight.get("Arrival")
    ordered_flight["DepTime"] = flight.get("DepTime")
    ordered_flight["ArrivalTime"] = flight.get("ArrivalTime")
    ordered_flight["Aircraft"] = flight.get("Aircraft")
    ordered_flight["Cockpit"] = flight.get("Cockpit")
    ordered_flight["Cabin"] = flight.get("Cabin")
    return ordered_flight


def reassemble_day(day: dict) -> OrderedDict:
    """
    Reassemble an individual day.
    If day has no flight times (FT_BLH, FDT, DT, RP are all None) and no flights,
    then return an OrderedDict with "IndividualDay", "Date", and "Duty": "Day Off".
    Otherwise, return with keys in this order:
      "IndividualDay", "Date", "FT_BLH", "FDT", "DT", "RP", "Flights"
    The "Flights" list is reassembled using reassemble_flight.
    """
    # Check for day off condition:
    times = [day.get("FT_BLH"), day.get("FDT"), day.get("DT"), day.get("RP")]
    flights = day.get("Flights", [])
    if all(time is None for time in times) and (not flights or len(flights) == 0):
        ordered_day = OrderedDict()
        ordered_day["IndividualDay"] = day.get("IndividualDay")
        ordered_day["Date"] = day.get("Date")
        ordered_day["Duty"] = "Day Off"
        return ordered_day

    # Otherwise, reassemble with all keys.
    ordered_day = OrderedDict()
    ordered_day["IndividualDay"] = day.get("IndividualDay")
    ordered_day["Date"] = day.get("Date")
    ordered_day["FT_BLH"] = day.get("FT_BLH")
    ordered_day["FDT"] = day.get("FDT")
    ordered_day["DT"] = day.get("DT")
    ordered_day["RP"] = day.get("RP")

    raw_flights = day.get("Flights", [])
    ordered_flights = []
    for flight in raw_flights:
        if isinstance(flight, dict):
            ordered_flights.append(reassemble_flight(flight))
        else:
            ordered_flights.append(flight)
    ordered_day["Flights"] = ordered_flights
    return ordered_day


def reassemble_statistics(stats: dict) -> OrderedDict:
    """
    Reassemble statistics in the desired order:
    "flightTimeBLH", "totalFlightTimeBLH", "dutyTime", "totalDutyTime",
    "paidLeave", "unpaidLeave", "illness", "dayOff"
    """
    ordered_stats = OrderedDict()
    ordered_stats["flightTimeBLH"] = stats.get("flightTimeBLH")
    ordered_stats["totalFlightTimeBLH"] = stats.get("totalFlightTimeBLH")
    ordered_stats["dutyTime"] = stats.get("dutyTime")
    ordered_stats["totalDutyTime"] = stats.get("totalDutyTime")
    ordered_stats["paidLeave"] = stats.get("paidLeave")
    ordered_stats["unpaidLeave"] = stats.get("unpaidLeave")
    ordered_stats["illness"] = stats.get("illness")
    ordered_stats["dayOff"] = stats.get("dayOff")
    return ordered_stats


@router.post("/schedule")
async def get_schedule():
    # Hardcoded user ID
    user_id = "6M7nQsnYefOHfnDQI94iWJUsUz53"

    # Reference to the schedules subcollection under /user/{user_id}
    schedules_ref = db.collection("user").document(user_id).collection("schedules")

    # Query the latest schedule document by ordering by timestamp descending
    docs = list(schedules_ref.order_by("timestamp", direction="DESCENDING").limit(1).stream())

    if not docs:
        return JSONResponse(content={"error": "No schedule found for user"}, status_code=404)

    # Extract the stored data (preferably from the "data" field)
    latest_doc = docs[0].to_dict()
    latest_data = latest_doc.get("data") or latest_doc

    # Reassemble statistics in the desired order.
    stats = latest_data.get("statistics", {})
    ordered_stats = reassemble_statistics(stats)

    # Reassemble the schedule list.
    raw_schedule = latest_data.get("schedule", [])
    ordered_schedule = []
    for day in raw_schedule:
        if isinstance(day, dict):
            ordered_schedule.append(reassemble_day(day))
        else:
            ordered_schedule.append(day)

    response_data = OrderedDict()
    response_data["statistics"] = ordered_stats
    response_data["schedule"] = ordered_schedule

    logging.info("Returning schedule response: %s", response_data)
    return JSONResponse(content=response_data)
