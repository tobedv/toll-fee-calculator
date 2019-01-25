import typing
import datetime
import json
import os
import argparse
from toll_calculator import TollCalculator
from vehicle_check import VehicleCheck, Vehicle
from csv_parser import CsvParser
from vehicle import Car, Motorbike


def _load_config(config_path: str) -> dict:
    """Load configuration from a specified configration path
    
    Args:
        config_path (str): local (UNIX) file path
    
    Raises:
        FileNotFoundError: If config is not found
    
    Returns:
        dict: A dictionary of config parameters
    """
    if not os.path.isfile(config_path):
        raise FileNotFoundError("Config file doesnt exist")
    with open(config_path) as f:
        return json.load(f)


def _get_vehicle_from_licence_plate(licence_plate: str) -> Vehicle:
    """Generates a Vehicle object based on a licence plate

    This Would most likely be replaced with an API call or simiar if this was
    an real life application
    
    See this as a placeholder, mockup.

    Args:
        licence_plate (str)
    
    Returns:
        Vehicle
    """
    vehicle_mappings = {"abc123": Car(), "abc321": Motorbike()}
    return vehicle_mappings[licence_plate]


def _get_vehicle_and_passes_from_csv(path_to_csv: str) -> typing.Tuple[Vehicle, list]:
    """Get data to be analyzed, will be parsed into a Vehicle object as well as a list of passes
    
    Args:
        path_to_csv (str)
    
    Returns:
        typing.Tuple[Vehicle, list]
    """

    cp = CsvParser()
    licence_plate, passes = cp.parse_csv(path_to_csv)
    return _get_vehicle_from_licence_plate(licence_plate), passes


def _get_total_daily_toll_for_vehicle(
    config: dict, vehicle: Vehicle, passes: typing.List[datetime.datetime]
) -> int:
    """If vehicle eligible for toll, calculate the daily total for that vehicle

    Args:
        config (dict)
        vehicle (Vehicle)
        passes (typing.List[datetime.datetime])

    Returns:
        int: Total cost
    """
    # Get year for the first item to get the correct taxes and free vehicles
    year = str(passes[0].year)
    vc = VehicleCheck(config[year])
    if vc.vehicle_eligible_for_toll(vehicle):
        tc = TollCalculator(config[year])
        return tc.get_daily_total_toll_fee(passes)
    else:
        return 0


def parse_csv_get_daily_toll(config_path: str, path_to_csv: str) -> int:
    """Wrapper to be called as the main funtion, will parse a given CSV file and return the daily total toll
    
    Args:
        config_path (str): Path to configuration file with tax, free vehicles and so on
        path_to_csv (str): File to be parsed and calculated upon
    
    Returns:
        int: Total cost
    """

    config = _load_config(config_path)
    vehicle, passes = _get_vehicle_and_passes_from_csv(path_to_csv)
    toll = _get_total_daily_toll_for_vehicle(config, vehicle, passes)
    return toll


def _initiate_arguments():
    parser = argparse.ArgumentParser(
        description=""":: Toll Calculator ::
Parses CSV with data containing passes and licence plate. 
Will give you a daily total of that vehicle.
The data currently needs to include only one licence plate and cannot handle several dates.

Asuage example:
python main.py /PATH/TO/CSV
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path_to_csv", type=str, help="Path to CSV to be parsed")
    return parser.parse_args()


if __name__ == "__main__":
    config_path = os.getenv(
        "TOLL_CALCULATOR_CONFIG_PATH",
        os.path.abspath(os.path.dirname(__file__)) + "/config.json",
    )
    args = _initiate_arguments()
    print(parse_csv_get_daily_toll(config_path, args.path_to_csv))
