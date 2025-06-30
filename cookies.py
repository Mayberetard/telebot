from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

cookies_collection = db["cookies"]
approved_users = db["approved_users"]

def add_cookie(user_id, cookie):
    cookies_collection.update_one({"user_id": user_id}, {"$set": {"cookie": cookie}}, upsert=True)

def get_cookie(user_id):
    doc = cookies_collection.find_one({"user_id": user_id})
    return doc["cookie"] if doc else None

def delete_cookie(user_id):
    cookies_collection.delete_one({"user_id": user_id})

def approve_user(user_id):
    approved_users.update_one({"user_id": user_id}, {"$set": {"approved": True}}, upsert=True)

def is_user_approved(user_id):
    return approved_users.find_one({"user_id": user_id, "approved": True}) is not None

def list_approved_users():
    return [doc["user_id"] for doc in approved_users.find()]
