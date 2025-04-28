from datetime import date, datetime
import unittest

from app.util import date_to_datetime, safe_file_name


class TestUtil(unittest.TestCase):
    ex1 = date(2012, 11, 10)
    def test_date_to_datetime(self):
        actual = date_to_datetime(self.ex1)
        self.assertIsInstance(self.ex1, date)
        self.assertIsInstance(actual, datetime)
        
        self.assertEqual(self.ex1.year, actual.year)
        self.assertEqual(self.ex1.month, actual.month)
        self.assertEqual(self.ex1.day, actual.day)
    
    def test_safe_file_name(self):
        self.assertEqual(safe_file_name("A B"), "A_B")
        self.assertEqual(safe_file_name("A B", lower=True), "a_b")
        self.assertEqual(safe_file_name("A.B"), "A_B")
        self.assertEqual(safe_file_name("A$B"), "A_B")
        self.assertEqual(safe_file_name("A B C"), "A_B_C")
        self.assertEqual(safe_file_name("A B C", lower=True), "a_b_c")
        self.assertEqual(safe_file_name("A\nB\tC"), "A_B_C")
        self.assertEqual(safe_file_name("x 1$2.3,4/5\\6\x00!7\t8[9]\rb"), "x_1_2_3_4_5_6__7_8_9__b")