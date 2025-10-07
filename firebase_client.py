# firebase_client.py

import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase Admin SDK
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': os.environ.get('FIREBASE_PROJECT_ID'),
})

db = firestore.client()

def get_db():
    return db
