import os
import sys
import pytest
import datetime

module_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(module_dir, "../src/"))
import main
import vehicle


def test__load_config():
    config_path = os.path.abspath(os.path.dirname(__file__)) + "/test_config.json"
    print(config_path)
    expected = {"test": 123}
    assert main._load_config(config_path)


def test__get_vehicle_and_passes_from_csv():
    test_csv = config_path = os.path.abspath(os.path.dirname(__file__)) + "/test.csv"
    expected_passes = [
        datetime.datetime(2019, 1, 23, 8, 0),
        datetime.datetime(2019, 1, 23, 9, 0),
    ]
    car = vehicle.Car()
    v, passes = main._get_vehicle_and_passes_from_csv(test_csv)
    assert car.get_type() == v.get_type()
    assert passes == expected_passes


def test__get_total_daily_toll_for_vehicle():
    config_path = os.path.abspath(os.path.dirname(__file__)) + "/full_test_config.json"
    cfg = main._load_config(config_path)
    car = vehicle.Car()
    # 16 sek
    passes = [
        datetime.datetime(2019, 1, 23, 8, 0),
        datetime.datetime(2019, 1, 23, 9, 0),
    ]
    assert main._get_total_daily_toll_for_vehicle(cfg, car, passes) == 16


def test_parse_csv_get_daily_toll():
    config_path = os.path.abspath(os.path.dirname(__file__)) + "/full_test_config.json"
    test_csv = os.path.abspath(os.path.dirname(__file__)) + "/test.csv"
    assert main.parse_csv_get_daily_toll(config_path, test_csv) == 16
