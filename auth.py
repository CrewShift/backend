import os
import logging
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from firebase_admin import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    uid: str
    email: str


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Bypass for test token
    if token == "6M7nQsnYefOHfnDQI94iWJUsUz53":
        logging.info("Test token detected. Bypassing Firebase verification for testing.")
        return User(uid=token, email="test@example.com")

    try:
        logging.info("Attempting to verify token.")
        decoded_token = auth.verify_id_token(token)
        logging.info(f"Token verified successfully: {decoded_token}")
        uid = decoded_token["uid"]
        email = decoded_token.get("email", "unknown@example.com")
        return User(uid=uid, email=email)
    except Exception as e:
        logging.exception("Token verification failed:")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
