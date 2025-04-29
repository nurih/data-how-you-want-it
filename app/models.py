import datetime
import json
from typing import Literal

from pydantic import BaseModel, Field, computed_field


class TicketCount(BaseModel):
    movie: str
    count: int = Field(..., ge=0)


class TheaterSales(BaseModel):
    theater: str
    day: datetime.date
    sales: list[TicketCount] = []

    @computed_field(alias="_id")
    @property
    def id(self) -> str:
        return create_id(self.theater, self.day)

    model_config = {
        "json_schema_extra": {
            "example": {
                "theater": "Cineplex",
                "day": "2012-12-20",
                "sales": [
                    {"movie": "The Dark Knight Rises", "count": 950},
                    {"movie": "Adventureland", "count": 234},
                ],
            }
        }
    }


def create_id(name: str, day: str | datetime.date):
    if isinstance(day, datetime.date):
        day = day.isoformat().lower()
    else:
        day = day.lower()
    return f"{day}_{name.lower().replace(' ', '_')}"


class BoxOfficeQueryOptions(BaseModel):
    breakdown: Literal["theater", "sales.movie"]


if __name__ == "__main__":
    schema = TheaterSales.model_json_schema()
    print(json.dumps(schema))
