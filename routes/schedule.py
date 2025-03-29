import os
import asyncio
import base64
import requests
import tempfile
from typing import List
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import storage

router = APIRouter()

@router.post("/schedule")
async def chat_endpoint():
    response_data = {
        "IndividualDay": "Wed, 02Apr",
        "Date": "2025-04-02",
        "FT_BLH": "05:55",
        "FDT": "07:55",
        "DT": "08:25",
        "RP": "17:30",
        "Flights": [
            {
                "Duty": "CAI8140",
                "CheckIn": "03:45",
                "CheckOut": None,
                "Departure": "SOF",
                "Arrival": "WAW",
                "DepTime": "04:45",
                "ArrivalTime": "07:45",
                "Aircraft": "A320/BHL",
                "Cockpit": "TRI G.GOSPODINOV; COP US R. BERNARDO",
                "Cabin": "SEN CCM S.ZHEKOVA; INS CCM A.IVANOVA; CCM 2 Y.BOEVA; CCM K.KALOYANOV; CCM M.ANDREEV; CCM UT K.KRUMOV; CCM UT V.PETROV"
            },
            {
                "Duty": "CAI8141",
                "CheckIn": None,
                "CheckOut": "12:10",
                "Departure": "WAW",
                "Arrival": "AYT",
                "DepTime": "08:45",
                "ArrivalTime": "11:10",
                "Aircraft": "A320/BHL",
                "Cockpit": "TRI G.GOSPODINOV; COP US R. BERNARDO",
                "Cabin": "SEN CCM S.ZHEKOVA; INS CCM A.IVANOVA; CCM 2 Y.BOEVA; CCM K.KALOYANOV; CCM M.ANDREEV; CCM UT K.KRUMOV; CCM UT V.PETROV"
            }
        ]
    }
    return JSONResponse(content=response_data)
