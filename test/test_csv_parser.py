import os
import sys
import pytest
import datetime

module_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(module_dir, "../src/"))
import csv_parser


@pytest.fixture
def parser():
    return csv_parser.CsvParser()


def test__convert_datestr_to_datetime(parser):
    date_str = "2019-01-01 12:00:00"
    expected = datetime.datetime(2019, 1, 1, 12)
    assert parser._convert_datestr_to_datetime(date_str) == expected


def test_parse_csv(parser):
    csv_path = os.path.abspath(os.path.dirname(__file__)) + "/test.csv"
    lp = "abc123"
    passes = [
        datetime.datetime(2019, 1, 23, 8, 0),
        datetime.datetime(2019, 1, 23, 9, 0),
    ]
    assert parser.parse_csv(csv_path) == (lp, passes)
