from database.connection import get_connection
from .queries import INSERT_USER
from models.user import User
from models.profile import Profile
from .userRepository import UserRepository
from .seederRepository import seederRepository
from models.scooter import Scooter
from models.traveller import Traveller



def seed_database():
    sr = seederRepository()
    ur = UserRepository()
    sys_admin = User.create(
        username="sysadmin01",
        password="StrongPass!123",
        role="system_admin",
        profile=Profile(first_name="Sharoek", last_name="Mahboeb")
    )

    ser_engineer = User.create(
        username="engineer1",
        password="StrongPass!123",
        role="service_engineer",
        profile=Profile(first_name="Dirk", last_name="Dikkie")
    )

    traveller1 = Traveller(
        customer_id=1,
        first_name="John",
        last_name="Doe",
        birthday="1990-01-01",
        gender="male",
        street_name="Main St",
        house_number="123",
        zip_code="2613JH",
        city="Amsterdam",
        email_address="john.doe@example.com",
        mobile_phone="81684567",
        driving_license_number="DD1234567"
    )

    traveller2 = Traveller(
        customer_id=2,
        first_name="Jane",
        last_name="Smith",
        birthday="1992-02-02",
        gender="female",
        street_name="Second St",
        house_number="456",
        zip_code="5541AD",
        city="Rotterdam",
        email_address="jane.smith@example.com",
        mobile_phone="89651234",
        driving_license_number="D98765432"
    )

    scooter1 = Scooter(
        brand="Segway",
        model="Ninebot Max G30",
        serial_number="SN1234567890ABC",
        top_speed=25,
        battery_capacity=551,
        state_of_charge=80,
        min_soc=20,
        max_soc=90,
        latitude=51.86001,
        longitude=4.40501,
        out_of_service_status=False,
        mileage=312.5,
        last_maintenance_date='2025-01-10'
    )

    scooter2 = Scooter(
        brand="Xiaomi",
        model="M365 Pro",
        serial_number="SN0987654321XYZ",
        top_speed=25,
        battery_capacity=474,
        state_of_charge=75,
        min_soc=20,
        max_soc=90,
        latitude=51.85661,
        longitude=4.51222,
        out_of_service_status=False,
        mileage=150.0,
        last_maintenance_date='2025-01-15'
    )


    sr.save_scooter_to_db(scooter1)
    sr.save_scooter_to_db(scooter2)
    sr.save_traveller_to_db(traveller1)
    sr.save_traveller_to_db(traveller2)
    ur.save_user_to_db(sys_admin)
    ur.save_user_to_db(ser_engineer)
    print("[i] Database seeded successfully.")