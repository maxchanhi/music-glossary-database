from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
def check_connection():
    uri = st.secrets["MONGODB_URI"]
    
    # Create a client with SSL enabled
    client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
