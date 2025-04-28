import asyncio
import os
from datetime import date
from motor.motor_asyncio import AsyncIOMotorClient
from app.models import TheaterSales
from app.util import date_to_datetime

CONNECTION_STRING = os.environ.get("MY_MONGODB_URI", "mongodb://localhost/demo")

client = AsyncIOMotorClient(CONNECTION_STRING)
db = client.get_default_database()


async def ping_cluster():
    result = await db.command("ping", check=True)
    return result


async def slam_one_sale(data: TheaterSales):
    sales = [m.model_dump() for m in data.sales]
    result = await db.theater_sales.update_one(
        {"_id": data.id},
        {
            "$set": {
                "sales": sales,
                "theater": data.theater,
                "day": date_to_datetime(data.day),
            }
        },
        upsert=True,
    )
    print("result %s" % repr(result.upserted_id))
    return result


async def add_theater_sales(b: TheaterSales):
    r = await db.theater_sales.update_one(
        {"_id": b.id},
        {
            "$set": {"theater": b.theater, "day": date_to_datetime(b.day)},
            "$push": {"sales": {"$each": [m.model_dump() for m in b.sales]}},
        },
        upsert=True,
    )
    print(r)
    return r


async def get_one_theater_sales(day: date, theater: str):
    """Get the sales for a single day."""

    filter = {"_id": f"{day}_{theater.lower().replace(' ','_')}"}

    doc = await db.theater_sales.find_one(filter)
    return doc if doc else None


async def multi_day_sales(on_or_after: date, before: date, breakdown: list[str]):
    """Get the box office sales for the given date range and breakdown."""

    filter = date_filter(on_or_after, before)
    unwind = unpivot_sales()
    group = group_by(breakdown)
    flatten = flatten_id()
    pipeline = [filter, unwind, group, flatten]

    print(pipeline)

    return await db.theater_sales.aggregate(pipeline).to_list(128)


def group_by(*args: str):
    """Group by the given fields and sum the ticket count.
    Args:
        *args: The fields to group by."""

    id = {k.replace(".", "_"): f"${k}" for k in args}
    return {"$group": {"_id": id, "sold": {"$sum": "$sales.count"}}}


def date_filter(on_or_after, before):
    return {
        "$match": {
            "day": {
                "$gte": date_to_datetime(on_or_after),
                "$lt": date_to_datetime(before),
            }
        }
    }


def unpivot_sales():
    return {"$unwind": "$sales"}


def flatten_id():
    return {"$replaceRoot": {"newRoot": {"$mergeObjects": ["$_id", {"sold": "$sold"}]}}}


async def _main():
    available_collections = await db.list_collection_names()

    print("Will use ", client.HOST, client.PORT, "and namespaces:", db.name)
    print("DB has collections:", available_collections)
    c = db.marp
    print(c.name)
    print(c.database.name)


if __name__ == "__main__":
    asyncio.run(_main())
