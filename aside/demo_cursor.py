import os
import pprint
import asyncio

from pymongo import AsyncMongoClient

CONNECTION_STRING = os.environ.get("MY_MONGODB_URI", "mongodb://localhost/demo")

client = AsyncMongoClient(CONNECTION_STRING)

db = client.get_default_database()
print(db)

collection = db.get_collection("theater_sales")
print(collection)


async def print_sales_docs(max_docs: int):

    print("Calling find returns a cursor")
    cursor = collection.find({})

    print("Async cursor iteration:")
    for document in await cursor.to_list(length=max_docs):
        pprint.pprint(document)


asyncio.run(print_sales_docs(max_docs=10))
