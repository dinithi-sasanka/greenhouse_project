# utils/db.py
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# -------------------------------
# LOAD ENVIRONMENT VARIABLES
# -------------------------------
load_dotenv()
client = MongoClient(
    "mongodb+srv://dinithisasanka01_db_user:dinithi2005@greenhouse.svuv3cn.mongodb.net/greenhouse_db?retryWrites=true&w=majority",
    tls=True,
    tlsAllowInvalidCertificates=True  
)
 
# -------------------------------
# MONGODB CONNECTION
# -------------------------------
client = MongoClient("mongodb+srv://dinithisasanka01_db_user:dinithi2005@greenhouse.svuv3cn.mongodb.net/greenhouse_db?retryWrites=true&w=majority")
db = client['greenhouse_db']       
users_col = db['users']            

# -------------------------------
# FETCH ALL USERS
# -------------------------------
def fetch_users():
    """Return all users as a list of dicts."""
    return list(users_col.find())

# -------------------------------
# ADD USER
# -------------------------------
def add_user(username, password, role, email, address, telephone):
    """Add a new user with hashed password."""
    hashed_pwd = generate_password_hash(password)
    users_col.insert_one({
        "username": username,
        "password": hashed_pwd,
        "role": role,
        "email": email,
        "address": address,
        "telephone": telephone
    })

# -------------------------------
# DELETE USER
# -------------------------------
def delete_user(user_id):
    """Delete a user by ObjectId string."""
    users_col.delete_one({"_id": ObjectId(user_id)})

# -------------------------------
# UPDATE USER
# -------------------------------
def update_user(user_id, username, role, email, address, telephone, password=None):
    """Update user details. Hash password if provided."""
    update_data = {
        "username": username,
        "role": role,
        "email": email,
        "address": address,
        "telephone": telephone
    }
    if password:
        update_data["password"] = generate_password_hash(password)
    users_col.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

# -------------------------------
# SEARCH USERS
# -------------------------------
def search_users(keyword):
    """Search users by username, email, role, or telephone (case-insensitive)."""
    query = {
        "$or": [
            {"username": {"$regex": keyword, "$options": "i"}},
            {"email": {"$regex": keyword, "$options": "i"}},
            {"role": {"$regex": keyword, "$options": "i"}},
            {"telephone": {"$regex": keyword, "$options": "i"}}
        ]
    }
    return list(users_col.find(query))

# -------------------------------
# VALIDATE LOGIN
# -------------------------------
def validate_user(username, password):
    """Check if username exists and password matches. Return user dict if valid, else None."""
    user = users_col.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        return user
    return None

# -------------------------------
# FETCH SINGLE USER BY USERNAME
# -------------------------------
def fetch_user_by_username(username):
    """Return a single user dict by username."""
    return users_col.find_one({"username": username})

# -------------------------------
# RESET USER PASSWORD
# -------------------------------
def update_user_password(username, new_password):
    """Update user's password with hashed new password."""
    hashed = generate_password_hash(new_password)
    users_col.update_one({"username": username}, {"$set": {"password": hashed}})
