import re

def validate_username(username: str) -> bool:
    """
    Validates the username according to assignment rules:
    - 8 to 10 characters long
    - Starts with a letter or underscore
    - Contains only letters, digits, underscores, apostrophes, or periods
    - Case-insensitive (handled elsewhere)
    """
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_.'']{7,9}$"
    return re.fullmatch(pattern, username) is not None

def validate_password(password: str) -> bool:
    """
    Validates the password according to assignment rules:
    - 12 to 30 characters
    - At least one lowercase letter
    - At least one uppercase letter
    - At least one digit
    - At least one special character
    """
    if not (12 <= len(password) <= 30):
        return False

    # Must contain lowercase, uppercase, digit, special character
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,30}$"
    return re.fullmatch(pattern, password) is not None

def validate_zip_code(zip_code: str) -> bool:
    return re.fullmatch(r"^\d{4}[A-Z]{2}$", zip_code) is not None

def validate_mobile(phone: str) -> bool:
    """
    Checks if user input is 8 digits (for +31-6-DDDDDDDD)
    """
    return re.fullmatch(r"^\d{8}$", phone) is not None

def validate_driving_license(dl: str) -> bool:
    """
    Format:
    - XXDDDDDDD (2 letters, 7 digits)
    - OR XDDDDDDDD (1 letter, 8 digits)
    """
    return re.fullmatch(r"^[A-Z]{1,2}\d{7,8}$", dl) is not None
