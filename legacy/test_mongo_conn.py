from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

uri = "mongodb+srv://Vercel-Admin-atlas-amber-gardenc:XGrObDyQBHhk9TN5@atlas-amber-gardenc.ff23ewx.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(uri)
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("MongoDB connection successful!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
