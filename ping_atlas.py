from pymongo import MongoClient
import sys

try:
    client = MongoClient('mongodb+srv://sainlucky489_db_user:Ab33DkX8c7Mj2vdW@aikarmayogi.ruao4nw.mongodb.net/?retryWrites=true&w=majority', serverSelectionTimeoutMS=5000)
    db = client['ai_karmayogi']
    count = db.users.count_documents({})
    print(f"ATLAS ONLINE. Users: {count}")
    sys.exit(0)
except Exception as e:
    print(f"ATLAS OFFLINE: {e}")
    sys.exit(1)
