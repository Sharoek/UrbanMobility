from dataclasses import dataclass
from typing import Optional


@dataclass
class Scooter:
    id: Optional[int] = None
    brand: str = ""
    model: str = ""
    serial_number: str = ""
    top_speed: float = 0.0
    battery_capacity: float = 0.0
    state_of_charge: float = 0.0
    min_soc: float = 0.0
    max_soc: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0
    out_of_service_status: bool = False
    mileage: float = 0.0
    last_maintenance_date: str = ""


 


        