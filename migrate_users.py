import pandas as pd
from pymongo import MongoClient

# -------------------------------
# MongoDB Connection
# -------------------------------
MONGO_URI = "mongodb+srv://dinithisasanka01_db_user:dinithi2005@greenhouse.svuv3cn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['greenhouse_db']   # MongoDB database
users_col = db['users']        # Users collection

# -------------------------------
# Load CSV
# -------------------------------
csv_file = r"C:\Users\Acer\Downloads\allUsers.csv"  # Your CSV path
df = pd.read_csv(csv_file)

# -------------------------------
# Insert into MongoDB
# -------------------------------
for _, row in df.iterrows():
    users_col.insert_one({
        "username": row["username"],
        "password": row["password"],  # Already hashed in PostgreSQL
        "role": row["role"],
        "email": row["email"],
        "address": row["address"],
        "telephone": str(row["telephone"])  # Ensure string
    })

print("Migration complete! Users added to MongoDB.")
