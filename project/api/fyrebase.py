import os

import pyrebase

from .utils import validate_env_variables


validate_env_variables(
    [
        "FIREBASE_API_KEY",
        "FIREBASE_AUTH_DOMAIN",
        "FIREBASE_DATABASE_URL",
        "FIREBASE_PROJECT_ID",
        "FIREBASE_STORAGE_BUCKET",
        "FIREBASE_MESSAGING_SENDER_ID",
        "FIREBASE_APP_ID",
    ]
)


# Descomente a linha abaixo e atualize com as suas credenciais Firebase
firebaseConfig = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
}

firebase = pyrebase.initialize_app(config=firebaseConfig)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()
