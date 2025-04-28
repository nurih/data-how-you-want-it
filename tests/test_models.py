from datetime import date, datetime
import unittest

from app.models import TheaterSales, TicketCount, create_id
from app.util import date_to_datetime


class TestTheaterSales(unittest.TestCase):

    ex1 = TheaterSales(
        theater="Broadway Theater",
        day=date(2012, 11, 10),
        sales=[
            TicketCount(movie="The Dark Knight Rises", count=12),
            TicketCount(movie="Adventureland", count=34),
            TicketCount(movie="Anything's Possible", count=56),
        ],
    )

    expected_composed_id = "2012-11-10_broadway_theater"

    def test_id_composition(self):
        self.assertEqual(self.ex1.id, self.expected_composed_id)

    def test_dumps_as_underscore_id(self):
        dumped = self.ex1.model_dump()
        self.assertEqual(dumped.get("id"), self.expected_composed_id)

    def test_create_id_with_string_day(self):
        self.assertEqual(create_id("A B", "2000-01-02"), "2000-01-02_a_b")

    def test_create_id_with_date_day(self):
        self.assertEqual(create_id("X", date(2020, 12, 26)), "2020-12-26_x")

