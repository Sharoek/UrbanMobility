from dataclasses import dataclass, field
from datetime import datetime
import hashlib
from typing import Optional
from .profile import Profile

@dataclass
class User:
    username: str
    password_hash: str
    role: str

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def create(cls, username: str, password: str, role: str, profile: Optional[Profile] = None):
        pw_hash = cls.hash_password(password)
        if role == 'super_admin':
            return SuperAdmin(username, pw_hash)
        elif role == 'system_admin':
            return SystemAdmin(username, pw_hash, profile)
        elif role == 'service_engineer':
            return ServiceEngineer(username, pw_hash, profile)
        else:
            raise ValueError(f"Unknown role {role}")

@dataclass
class SuperAdmin(User):
    """
    A Super Administrator has full 
    control of the system. In practice, 
    their main role is to create and 
    manage System Administrator 
    accounts
    """
    def __init__(self, username: str, password_hash: str):
        super().__init__(username, password_hash, role='super_admin')

@dataclass
class SystemAdmin(User):
    """
    A System Administrator can 
    manage Service Engineer
    accounts and add, update and 
    delete scooter information.
    """
    profile: Profile
    def __init__(self, username: str, password_hash: str, profile: Profile):
        super().__init__(username, password_hash, role='system_admin')
        self.profile = profile

@dataclass
class ServiceEngineer(User):
    """
    A Service Engineer can fully 
    manage Traveler accounts and 
    update some attributes of existing 
    scooter information. They are not 
    allowed to add or delete scooters.
    """
    profile: Profile
    def __init__(self, username: str, password_hash: str, profile: Profile):
        super().__init__(username, password_hash, role='service_engineer')
        self.profile = profile