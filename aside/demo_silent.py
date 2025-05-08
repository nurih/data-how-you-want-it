import os

from motor.motor_asyncio import AsyncIOMotorClient

CONNECTION_STRING = os.environ.get("MY_MONGODB_URI", "mongodb://localhost/demo")

client = AsyncIOMotorClient(CONNECTION_STRING)

db = client.get_default_database()
print(db)

collection = db.get_collection("some_random_name")
print(collection)
