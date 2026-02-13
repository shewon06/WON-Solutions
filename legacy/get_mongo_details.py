from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

uri = "mongodb+srv://Vercel-Admin-atlas-amber-gardenc:XGrObDyQBHhk9TN5@atlas-amber-gardenc.ff23ewx.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(uri)
    # Trigger connection
    client.admin.command('ismaster')
    print(f"Replica Set: {client.primary}")
    print(f"Nodes: {client.nodes}")
    # Get replica set name from ismaster response
    res = client.admin.command('ismaster')
    print(f"ReplicaSetName: {res.get('setName')}")
    print("MongoDB connection successful!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
