import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("secrets\notification-system-42053-firebase-adminsdk-fbsvc-089bd951b6.json")
        firebase_admin.initialize_app(cred)