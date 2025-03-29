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

# schedule endopint
@router.post("/schedule")
async def chat_endpoint():
    response_data = [
        {
            "IndividualDay": "Mon, 01Apr",
            "Date": "2025-04-01",
            "FT_BLH": "05:55",
            "FDT": "07:55",
            "DT": "08:25",
            "RP": "17:30",
            "Flights": [
                {
                    "Duty": "CAI8001",
                    "CheckIn": "03:45",
                    "CheckOut": None,
                    "Departure": "SOF",
                    "Arrival": "WAW",
                    "DepTime": "04:45",
                    "ArrivalTime": "07:45",
                    "Aircraft": "A320/BHL",
                    "Cockpit": "TRI G.GOSPODINOV; COP US R. BERNARDO",
                    "Cabin": "SEN CCM S.ZHEKOVA; INS CCM A.IVANOVA; CCM K.KALOYANOV"
                },
                {
                    "Duty": "CAI8002",
                    "CheckIn": None,
                    "CheckOut": "12:10",
                    "Departure": "WAW",
                    "Arrival": "AYT",
                    "DepTime": "08:30",
                    "ArrivalTime": "10:45",
                    "Aircraft": "A320/BHL",
                    "Cockpit": "TRI G.GOSPODINOV; COP US R. BERNARDO",
                    "Cabin": "SEN CCM S.ZHEKOVA; CCM 2 Y.BOEVA; CCM M.ANDREEV"
                }
            ]
        },
        {
            "IndividualDay": "Tue, 02Apr",
            "Date": "2025-04-02",
            "FT_BLH": "06:10",
            "FDT": "08:00",
            "DT": "08:40",
            "RP": "18:00",
            "Flights": [
                {
                    "Duty": "CAI8011",
                    "CheckIn": "04:00",
                    "CheckOut": None,
                    "Departure": "SOF",
                    "Arrival": "FRA",
                    "DepTime": "05:00",
                    "ArrivalTime": "07:15",
                    "Aircraft": "B737/ATR",
                    "Cockpit": "CAPT L.KOSTADINOVA; FO A.PETROV",
                    "Cabin": "SEN CCM M.IVANOVA; CCM 2 P.DIMITROV"
                },
                {
                    "Duty": "CAI8012",
                    "CheckIn": None,
                    "CheckOut": "13:00",
                    "Departure": "FRA",
                    "Arrival": "SOF",
                    "DepTime": "08:00",
                    "ArrivalTime": "10:10",
                    "Aircraft": "B737/ATR",
                    "Cockpit": "CAPT L.KOSTADINOVA; FO A.PETROV",
                    "Cabin": "SEN CCM M.IVANOVA; CCM 2 P.DIMITROV"
                }
            ]
        },
        {
            "IndividualDay": "Wed, 03Apr",
            "Date": "2025-04-03",
            "Duty": "Day Off"
        },
        {
            "IndividualDay": "Thu, 04Apr",
            "Date": "2025-04-04",
            "FT_BLH": "06:05",
            "FDT": "08:10",
            "DT": "08:40",
            "RP": "16:00",
            "Flights": [
                {
                    "Duty": "CAI8031",
                    "CheckIn": "04:15",
                    "CheckOut": None,
                    "Departure": "SOF",
                    "Arrival": "LHR",
                    "DepTime": "05:15",
                    "ArrivalTime": "07:20",
                    "Aircraft": "A320/BHL",
                    "Cockpit": "TRI G.GOSPODINOV; COP US R. BERNARDO",
                    "Cabin": "SEN CCM S.ZHEKOVA; INS CCM A.IVANOVA; CCM UT V.PETROV"
                },
                {
                    "Duty": "CAI8032",
                    "CheckIn": None,
                    "CheckOut": "13:20",
                    "Departure": "LHR",
                    "Arrival": "SOF",
                    "DepTime": "08:30",
                    "ArrivalTime": "11:00",
                    "Aircraft": "A320/BHL",
                    "Cockpit": "TRI G.GOSPODINOV; COP US R. BERNARDO",
                    "Cabin": "SEN CCM S.ZHEKOVA; INS CCM A.IVANOVA; CCM UT V.PETROV"
                }
            ]
        },
        {
            "IndividualDay": "Fri, 05Apr",
            "Date": "2025-04-05",
            "FT_BLH": "05:45",
            "FDT": "07:50",
            "DT": "08:20",
            "RP": "14:30",
            "Flights": [
                {
                    "Duty": "CAI8041",
                    "CheckIn": "02:40",
                    "CheckOut": None,
                    "Departure": "SOF",
                    "Arrival": "CDG",
                    "DepTime": "03:40",
                    "ArrivalTime": "06:10",
                    "Aircraft": "A320/BHL",
                    "Cockpit": "CAPT N.STOYANOV; FO R.IVANOV",
                    "Cabin": "SEN CCM T.PETROVA; INS CCM K.DIMITROVA"
                },
                {
                    "Duty": "CAI8042",
                    "CheckIn": None,
                    "CheckOut": "11:25",
                    "Departure": "CDG",
                    "Arrival": "SOF",
                    "DepTime": "07:00",
                    "ArrivalTime": "09:25",
                    "Aircraft": "A320/BHL",
                    "Cockpit": "CAPT N.STOYANOV; FO R.IVANOV",
                    "Cabin": "SEN CCM T.PETROVA; INS CCM K.DIMITROVA"
                }
            ]
        },
        {
            "IndividualDay": "Sat, 06Apr",
            "Date": "2025-04-06",
            "FT_BLH": "06:00",
            "FDT": "08:05",
            "DT": "08:35",
            "RP": "16:20",
            "Flights": [
                {
                    "Duty": "CAI8051",
                    "CheckIn": "03:55",
                    "CheckOut": None,
                    "Departure": "SOF",
                    "Arrival": "WAW",
                    "DepTime": "04:55",
                    "ArrivalTime": "07:50",
                    "Aircraft": "B777/ERJ",
                    "Cockpit": "CAPT I.KOLYADIN; FO D.PETROVA",
                    "Cabin": "SEN CCM L.GEORGIEVA; INS CCM M.KARPOV; CCM 2 I.NIKOLSKA"
                },
                {
                    "Duty": "CAI8052",
                    "CheckIn": None,
                    "CheckOut": "12:45",
                    "Departure": "WAW",
                    "Arrival": "SOF",
                    "DepTime": "08:50",
                    "ArrivalTime": "11:05",
                    "Aircraft": "B777/ERJ",
                    "Cockpit": "CAPT I.KOLYADIN; FO D.PETROVA",
                    "Cabin": "SEN CCM L.GEORGIEVA; INS CCM M.KARPOV; CCM 2 I.NIKOLSKA"
                }
            ]
        },
        {
            "IndividualDay": "Sun, 07Apr",
            "Date": "2025-04-07",
            "FT_BLH": "05:50",
            "FDT": "07:45",
            "DT": "08:15",
            "RP": "15:40",
            "Flights": [
                {
                    "Duty": "CAI8061",
                    "CheckIn": "02:35",
                    "CheckOut": None,
                    "Departure": "SOF",
                    "Arrival": "LHR",
                    "DepTime": "03:35",
                    "ArrivalTime": "06:10",
                    "Aircraft": "A320/BHL",
                    "Cockpit": "CAPT V.DIMOV; FO S.PETROV",
                    "Cabin": "SEN CCM R.KOSTADINOVA; CCM 2 T.NIKOLSKA"
                },
                {
                    "Duty": "CAI8062",
                    "CheckIn": None,
                    "CheckOut": "11:40",
                    "Departure": "LHR",
                    "Arrival": "SOF",
                    "DepTime": "07:00",
                    "ArrivalTime": "10:00",
                    "Aircraft": "A320/BHL",
                    "Cockpit": "CAPT V.DIMOV; FO S.PETROV",
                    "Cabin": "SEN CCM R.KOSTADINOVA; CCM 2 T.NIKOLSKA"
                }
            ]
        },
        {
            "IndividualDay": "Mon, 08Apr",
            "Date": "2025-04-08",
            "Duty": "Day Off"
        },
        {
            "IndividualDay": "Tue, 09Apr",
            "Date": "2025-04-09",
            "FT_BLH": "05:40",
            "FDT": "07:35",
            "DT": "08:05",
            "RP": "14:50",
            "Flights": [
                {
                    "Duty": "CAI8081",
                    "CheckIn": "03:30",
                    "CheckOut": None,
                    "Departure": "SOF",
                    "Arrival": "WAW",
                    "DepTime": "04:30",
                    "ArrivalTime": "07:20",
                    "Aircraft": "A320/BHL",
                    "Cockpit": "CAPT M.TODOROV; FO E.KOSTADINOVA",
                    "Cabin": "SEN CCM P.STOILOV; CCM 2 G.PETROVA"
                },
                {
                    "Duty": "CAI8082",
                    "CheckIn": None,
                    "CheckOut": "12:20",
                    "Departure": "WAW",
                    "Arrival": "SOF",
                    "DepTime": "08:00",
                    "ArrivalTime": "10:10",
                    "Aircraft": "A320/BHL",
                    "Cockpit": "CAPT M.TODOROV; FO E.KOSTADINOVA",
                    "Cabin": "SEN CCM P.STOILOV; CCM 2 G.PETROVA"
                }
            ]
        }
    ]
    return JSONResponse(content=response_data)
