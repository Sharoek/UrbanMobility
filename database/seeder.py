from database.connection import get_connection
from .queries import INSERT_USER
from models.user import User
from models.profile import Profile
from .repositories import UserRepository



def seed_database():
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

    ur.save_user_to_db(sys_admin)
    ur.save_user_to_db(ser_engineer)


        
