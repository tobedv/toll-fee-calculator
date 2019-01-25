import os
import sys
import pytest

module_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(module_dir, "../src/"))
import vehicle_check
import vehicle


@pytest.fixture
def checker():
    cfg = {
        "toll_free_vehicles": [
            "Motorbike",
            "Tractor",
            "Emergency",
            "Diplomat",
            "Foreign",
            "Military",
        ]
    }
    yield vehicle_check.VehicleCheck(cfg)


def test_vehicle_eligible_for_toll(checker):
    assert checker.vehicle_eligible_for_toll(vehicle.Motorbike()) is False
