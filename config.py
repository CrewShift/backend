from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FIREBASE_CREDENTIALS: str = "crewshift-app-firebase-adminsdk-fbsvc-ece9f6e2b1.json"
    FIREBASE_STORAGE_BUCKET: str = 'crewshift-app.firebasestorage.app'
    HOST: str = "0.0.0.0"
    PORT: int = 8000

settings = Settings()