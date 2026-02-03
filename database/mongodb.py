

from pymongo import MongoClient
import os

def get_collection():
    mongo_uri = os.getenv("MONGO_URI")

    client = MongoClient(mongo_uri)  # 🔥 DO NOT ADD TLS OPTIONS

    db = client["sample_mflix"]         # Database Name
    return db["KnowledgeBase"]         # Collection Name