# auth.py
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
    if token == "p949ztzNnEh1hfe0knLng9EuAcp1":
        logging.info("Test token detected. Bypassing Firebase verification for testing.")
        return {"uid": token, "email": "test@example.com"}
    try:
        logging.info("Attempting to verify token.")
        decoded_token = auth.verify_id_token(token)
        logging.info(f"Token verified successfully: {decoded_token}")
        uid = decoded_token["uid"]
        email = decoded_token.get("email")
        return {"uid": uid, "email": email}  # Returning as a dict for simplicity.
    except auth.RevokedIdTokenError:
        logging.error("Token has been revoked.")
        raise HTTPException(status_code=401, detail="Token has been revoked")
    except auth.ExpiredIdTokenError:
        logging.error("Token has expired.")
        raise HTTPException(status_code=401, detail="Token has expired")
    except auth.InvalidIdTokenError:
        logging.error("Invalid token.")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logging.error(f"Token verification failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
