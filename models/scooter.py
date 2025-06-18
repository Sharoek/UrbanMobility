from dataclasses import dataclass


@dataclass
class Scooter:
    id: int
    brand: str
    model: str
    serial_number: str
    top_speed: float
    battery_capacity: float
    state_of_charge: float
    min_soc: float
    max_soc: float
    latitude: float
    longitude: float
    out_of_service_status: bool
    mileage: float
    last_maintenance_date: str

    def _init_(self, id: int, brand: str, model: str, serial_number: str, top_speed: float,
                 battery_capacity: float, state_of_charge: float, min_soc: float, max_soc: float,
                 latitude: float, longitude: float, out_of_service_status: bool, mileage: float,
                 last_maintenance_date: str):
        self.id = id
        self.brand = brand
        self.model = model
        self.serial_number = serial_number
        self.top_speed = top_speed
        self.battery_capacity = battery_capacity
        self.state_of_charge = state_of_charge
        self.min_soc = min_soc
        self.max_soc = max_soc
        self.latitude = latitude
        self.longitude = longitude
        self.out_of_service_status = out_of_service_status
        self.mileage = mileage
        self.last_maintenance_date = last_maintenance_date

        