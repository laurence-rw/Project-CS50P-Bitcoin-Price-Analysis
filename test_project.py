import unittest
from unittest.mock import mock_open, patch
import datetime

from project import read_csv, convert_to_datetime, calculate_percentage_changes, count_jumps_within_ranges

class TestReadCSV(unittest.TestCase):
    def test_read_csv(self):
        # Test read_csv function
        csv_data = "snapped_at,price,market_cap,total_volume\n2013-04-28 00:00:00 UTC,135.3,1500517590,0\n2013-04-29 00:00:00 UTC,141.96,1575032004.0,0.0\n2013-04-30 00:00:00 UTC,135.3,1501657493.0,0.0"
        expected_output = [
            {"snapped_at": "2013-04-28 00:00:00 UTC", "price": "135.3", "market_cap": "1500517590", "total_volume": "0"},
            {"snapped_at": "2013-04-29 00:00:00 UTC", "price": "141.96", "market_cap": "1575032004.0", "total_volume": "0.0"},
            {"snapped_at": "2013-04-30 00:00:00 UTC", "price": "135.3", "market_cap": "1501657493.0", "total_volume": "0.0"}
        ]

        with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
            data = read_csv("dummy.csv")
            self.assertEqual(data, expected_output)

class TestConvertToDatetime(unittest.TestCase):
    def test_convert_to_datetime(self):
        # Test convert_to_datetime function
        data = [
            {"snapped_at": "2013-04-28 00:00:00 UTC"},
            {"snapped_at": "2013-04-29 00:00:00 UTC"}
        ]
        expected_output = [
            {"snapped_at": datetime.datetime(2013, 4, 28, 0, 0)},
            {"snapped_at": datetime.datetime(2013, 4, 29, 0, 0)}
        ]
        converted_data = convert_to_datetime(data)
        self.assertEqual(converted_data, expected_output)

class TestCalculatePercentageChanges(unittest.TestCase):
    def test_calculate_percentage_changes(self):
        # Test calculate_percentage_changes function
        data = [
            {"price": 100},
            {"price": 120},
            {"price": 110}
        ]
        expected_output = [20.0, -8.333333333333332]
        percentage_changes = calculate_percentage_changes(data)
        self.assertEqual(percentage_changes, expected_output)

class TestCountJumpsWithinRanges(unittest.TestCase):
    def test_count_jumps_within_ranges(self):
        # Test count_jumps_within_ranges function
        percentage_changes = [0.5, 1.5, 3.5, 5.5, 10.5]
        ranges = [(0, 1), (1, 3), (3, 6), (6, 10), (10, 15), (15, 25), (25, 50)]
        expected_output = {(0, 1): 1, (1, 3): 1, (3, 6): 2, (6, 10): 0, (10, 15): 1, (15, 25): 0, (25, 50): 0}
        jump_counts = count_jumps_within_ranges(percentage_changes, ranges)
        self.assertEqual(jump_counts, expected_output)

if __name__ == '__main__':
    unittest.main()
