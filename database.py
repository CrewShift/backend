import firebase_admin
from firebase_admin import credentials, firestore, storage
from config import settings

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred, {
    'projectId': 'crewshift-app',
    'storageBucket': settings.FIREBASE_STORAGE_BUCKET
})

db = firestore.client()
# bucket = storage.bucket()

from firebase_admin import firestore

# Access Firestore
# db = firestore.client()

def save_to_firestore(doc_ref, data):
    doc_ref.set(data)
