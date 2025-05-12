import os

from pymongo import AsyncMongoClient

CONNECTION_STRING = os.environ.get("MY_MONGODB_URI", "mongodb://localhost/demo")

client = AsyncMongoClient(CONNECTION_STRING)

db = client.get_default_database()
print(db)

collection = db.get_collection("some_random_name")
print(collection)
