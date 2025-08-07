from pymongo import MongoClient
from config import MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client["pinterest_bot"]
users = db["users"]

def add_user(user_id):
    if not users.find_one({"_id": user_id}):
        users.insert_one({"_id": user_id})