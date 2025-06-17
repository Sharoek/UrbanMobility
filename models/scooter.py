from dataclasses import dataclass


@dataclass
class Scooter:
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
