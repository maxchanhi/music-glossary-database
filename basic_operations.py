import datetime   # This will be needed later
import os
from dictionary_databse import data
from pprint import pprint
from dotenv import load_dotenv
from pymongo import MongoClient

# Load config from a .env file:
load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

client = MongoClient(MONGODB_URI)
db = client['music_terms']
music_terms = db['terms']

# Insert data into the collection
#insert_result = music_terms.insert_many(data)

# Print the IDs of the inserted documents
print("Inserted document IDs:")
#pprint(insert_result.inserted_ids)

# Preview the inserted data
print("\nPreview of inserted data:")
for doc in music_terms.find():
    pprint(doc)
