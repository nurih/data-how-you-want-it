from datetime import date, datetime
from unittest import IsolatedAsyncioTestCase

from app.mdb import (
    date_filter,
    group_by,
    get_one_theater_sales,
    unpivot_sales,
    flatten_id,
)


class TestMdb(IsolatedAsyncioTestCase):


    def test_groupby_id_multiple_fileds(self):
        """Test the group_by function with multiple fields."""
        actual = group_by("one.two")
        self.assertEqual(actual["$group"]["$_id"], {"one_two": "$one.two"})

    def test_groupby_id_single_filed(self):
        """Test the group_by function with single field."""

        expected = {
            "$group": {
                "_id": {"something": "$something"},
                "sold": {"$sum": "$sales.count"},
            }
        }
        actual = group_by("something")
        self.assertEqual(actual, expected)

    def test_groupby_id_multiple_fileds(self):
        """Test the group_by function with multiple fields."""
        expected = {
            "$group": {
                "_id": {"a_b": "$a.b", "c": "$c"},
                "sold": {"$sum": "$sales.count"},
            }
        }
        actual = group_by("a.b", "c")
        self.assertEqual(actual, expected)

    def test_date_filter(self):
        """Test the date_filter function."""
        on_or_after = datetime(2023, 1, 1)
        before = datetime(2023, 12, 31)
        expected = {
            "$match": {
                "day": {
                    "$gte": on_or_after,
                    "$lt": before,
                }
            }
        }
        actual = date_filter(on_or_after, before)
        self.assertEqual(actual, expected)
        self.assertIsInstance(actual["$match"]["day"]["$gte"], datetime)
        self.assertIsInstance(actual["$match"]["day"]["$lt"], datetime)

    def test_unpivot_sales(self):
        """Test the unpivot_sales function."""
        actual = unpivot_sales()

        self.assertEqual(actual, {"$unwind": "$sales"})

    def test_flatten_id(self):
        expected = {
            "$replaceRoot": {"newRoot": {"$mergeObjects": ["$_id", {"sold": "$sold"}]}}
        }

        self.assertEqual(flatten_id(), expected)
