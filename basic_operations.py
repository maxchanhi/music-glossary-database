import pymongo
from pymongo import MongoClient

def check_connection():
    uri = st.secrets["MONGODB_URI"]
    
    # Create a client with SSL enabled
    client = MongoClient(uri, ssl=True, ssl_cert_reqs='CERT_NONE')
    
    try:
        # Attempt to connect to the server
        db = client.test
        print("Connected to MongoDB!")
    except pymongo.errors.ServerSelectionTimeoutError as err:
        # Handle connection errors
        print("Failed to connect to MongoDB:", err)
