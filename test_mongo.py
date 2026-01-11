from pymongo import MongoClient

uri = "mongodb+srv://dinithisasanka01_db_user:dinithi2005@greenhouse.svuv3cn.mongodb.net/?appName=greenhouse"
client = MongoClient(uri)

db = client["greenhouse_db"]

print("Connected successfully!")
print("Collections:", db.list_collection_names())
