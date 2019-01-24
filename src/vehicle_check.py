from vehicle import Vehicle


class VehicleCheck:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.toll_free_vehicles = self.config["toll_free_vehicles"]

    def vehicle_eligible_for_toll(self, vehicle: Vehicle) -> bool:
        return vehicle.get_type() not in self.toll_free_vehicles
