from dataclasses import dataclass

@dataclass
class Traveller:
    customer_id: int
    first_name: str
    last_name: str
    birthday: str
    gender: str
    street_name: str
    house_number: str
    zip_code: str
    city: str
    email_address: str
    mobile_phone: str
    driving_license_number: str
