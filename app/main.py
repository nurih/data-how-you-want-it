from fastapi import status
from datetime import date
from typing import Annotated
from fastapi import FastAPI, HTTPException, Query

from pymongo.errors import ServerSelectionTimeoutError


from app.models import BoxOfficeQueryOptions, TheaterSales, TicketCount

from .mdb import (
    ping_cluster,
    add_theater_sales,
    get_one_theater_sales,
    multi_day_sales,
    slam_one_sale,
)

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})


@app.get("/ops/ping")
async def ping() -> bool:
    try:
        result = await ping_cluster()
        return result["ok"] == 1
    except ServerSelectionTimeoutError as sste:
        return False


@app.post("/movie/sale/{movie}/{theater}/")
async def handle_movie_sale_post(movie: str, theater: str):
    data = TheaterSales(
        theater=theater,
        day=date.today(),
        sales=[TicketCount(movie=movie, count=1)],
    )

    result = await slam_one_sale(data)

    return result.raw_result


@app.put("/theater_sales/")
async def handle_theater_sales_put(theater_sales: TheaterSales):
    """Insert or update a box office sale."""
    result = await add_theater_sales(theater_sales)

    return result.raw_result


@app.get(
    "/theater_sales/period/{on_or_after}/{strictly_before}/",
)
async def handle_theater_sales_period(
    on_or_after: date,
    strictly_before: date,
    options: Annotated[BoxOfficeQueryOptions, Query()],
) -> list[dict]:
    """Get the box office sales for the given date range and breakdown."""
    print(options.breakdown, type(options.breakdown))
    result = await multi_day_sales(on_or_after, strictly_before, options.breakdown)
    return result


@app.get("/theater_sales/{theater}/{day}/")
async def handle_theater_sales_for_one_day(theater: str, day: date):
    result = await get_one_theater_sales(day, theater)

    if result:
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "No record found", "criteria": [theater, day.isoformat()]},
    )
