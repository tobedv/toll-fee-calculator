import os
import sys
import pytest
import datetime

module_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(module_dir, "../src/"))
import toll_calculator


@pytest.fixture
def calculator():
    cfg = {
        "2019": {
            "max_daily_tax": 60,
            "tax": [
                {"start_time": "00:00", "end_time": "05:59", "price": 0},
                {"start_time": "06:00", "end_time": "06:29", "price": 9},
                {"start_time": "06:30", "end_time": "06:59", "price": 16},
                {"start_time": "07:00", "end_time": "07:59", "price": 22},
                {"start_time": "08:00", "end_time": "08:29", "price": 16},
                {"start_time": "08:30", "end_time": "14:59", "price": 9},
                {"start_time": "15:00", "end_time": "15:29", "price": 16},
                {"start_time": "15:30", "end_time": "16:59", "price": 22},
                {"start_time": "17:00", "end_time": "17:59", "price": 16},
                {"start_time": "18:00", "end_time": "18:29", "price": 9},
                {"start_time": "18:30", "end_time": "23:59", "price": 0},
            ],
        }
    }
    yield toll_calculator.TollCalculator(cfg)


def test__load_tax_mappings(calculator):
    calculator._load_tax_mappings("2019")
    expected_first = {
        "start_time": datetime.time(0, 0),
        "end_time": datetime.time(5, 59),
        "price": 0,
    }
    expected_fifth = {
        "start_time": datetime.time(8, 0),
        "end_time": datetime.time(8, 29),
        "price": 16,
    }
    assert calculator.taxes[0] == expected_first
    assert calculator.taxes[4] == expected_fifth


def test__get_toll_for_time(calculator):
    p = datetime.datetime(2019, 8, 11, 8, 11)
    assert calculator._get_toll_for_time(p) == 16


def test__calculate_max_toll_for_interval(calculator):
    # Mock underlying function, test isolated
    calculator._get_toll_for_time = lambda x: 30
    assert (
        calculator._calculate_max_toll_for_interval(
            [datetime.datetime(2019, 8, 11, 8, 11)]
        )
        == 30
    )


def test__build_date_intervals(calculator):
    start_date = datetime.datetime(2019, 1, 23, 8, 0)
    test_data = [
        # First group, all inside 60 minutes
        start_date,
        start_date + datetime.timedelta(minutes=20),
        start_date + datetime.timedelta(minutes=40),
        start_date + datetime.timedelta(minutes=60),
        # Second
        start_date + datetime.timedelta(minutes=65),
        start_date + datetime.timedelta(minutes=75),
        # Third
        start_date + datetime.timedelta(minutes=150),
    ]
    result = calculator._build_date_intervals(test_data)
    # Should be 3 intervals
    assert len(result) == 3
    print(result)
    # First interval should be 4 items
    assert len(result[0]) == 4
    # Second should be 2
    assert len(result[1]) == 2


# Full functional tests


def test_get_daily_total_toll_fee_under_max(calculator):
    # Wednesday, 08:00
    start_date = datetime.datetime(2019, 1, 23, 8, 0)

    # Total toll 34kr
    test_data = [
        # First group, 16kr
        start_date,
        start_date + datetime.timedelta(minutes=20),
        start_date + datetime.timedelta(minutes=40),
        start_date + datetime.timedelta(minutes=60),
        # Second, 9kr
        start_date + datetime.timedelta(minutes=65),
        start_date + datetime.timedelta(minutes=75),
        # Third, 9kr
        start_date + datetime.timedelta(minutes=150),
    ]
    assert calculator.get_daily_total_toll_fee(test_data) == 34


def test_get_daily_total_toll_fee_over_max(calculator):
    # Total 76 should equal maximum daily fee
    test_data = [
        # First 22kr
        datetime.datetime(2019, 1, 23, 7, 0),
        # Second 16kr
        datetime.datetime(2019, 1, 23, 8, 1),
        # Third 16kr
        datetime.datetime(2019, 1, 23, 15, 0),
        # Fourth 22kr
        datetime.datetime(2019, 1, 23, 16, 1),
    ]
    assert calculator.get_daily_total_toll_fee(test_data) == calculator.max_daily_tax
