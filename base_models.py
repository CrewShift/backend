from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict

class ImageUploadModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_img: UploadFile
    garment_img: UploadFile
    prompt: str

class User(BaseModel):
    uid: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UserAuth(BaseModel):
    email: str
    password: str
    goal: List[str]
    find_us: str
    gender: str
    referralCode: str = ""
