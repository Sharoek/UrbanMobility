from dataclasses import dataclass
from typing import Optional
from .profile import Profile
from encryption.hashing import hash_password  # bcrypt
from encryption.encryption import encrypt_data
from encryption.validators import validate_username, validate_password

@dataclass
class User:
    username: str
    password_hash: str
    role: str

    @classmethod
    def create(cls, username: str, password: str, role: str, profile: Optional[Profile] = None):
        if not validate_username(username):
            raise ValueError("Invalid username format")
        if not validate_password(password):
            raise ValueError("Invalid password format")

        pw_hash = hash_password(password)

        if role == 'super_admin':
            return SuperAdmin(username, pw_hash)
        elif role == 'system_admin':
            return SystemAdmin(username, pw_hash, profile)
        elif role == 'service_engineer':
            return ServiceEngineer(username, pw_hash, profile)
        else:
            raise ValueError(f"Unknown role '{role}'")

@dataclass
class SuperAdmin(User):
    def __init__(self, username: str, password_hash: str):
        super().__init__(username, password_hash, role='super_admin')

@dataclass
class SystemAdmin(User):
    profile: Profile
    def __init__(self, username: str, password_hash: str, profile: Profile):
        super().__init__(username, password_hash, role='system_admin')
        self.profile = profile

@dataclass
class ServiceEngineer(User):
    profile: Profile
    def __init__(self, username: str, password_hash: str, profile: Profile):
        super().__init__(username, password_hash, role='service_engineer')
        self.profile = profile
