from vehicle import Vehicle


class VehicleCheck:
    def __init__(self, config: dict) -> None:
        self.config = config
        # Lowercase all types to avoid typos in config
        self.toll_free_vehicles = [v.lower() for v in self.config["toll_free_vehicles"]]

    def vehicle_eligible_for_toll(self, vehicle: Vehicle) -> bool:
        """Check wether a Vehicle is eligable for being taxed when passing tolls
        
        Args:
            vehicle (Vehicle): Vehicle object should be checked
        
        Returns:
            bool: True if the Vehicle should receive toll, otherwise False
        """
        return vehicle.get_type().lower() not in self.toll_free_vehicles
