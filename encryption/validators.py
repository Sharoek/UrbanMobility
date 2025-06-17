import re

def validate_username(username: str) -> bool:
    """
    Validates the username:
    - 8 to 10 characters
    - Starts with a letter or underscore
    - Contains only letters, digits, underscores, apostrophes, or periods
    """
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_.'-]{7,9}$"
    return re.fullmatch(pattern, username) is not None

def validate_password(password: str) -> bool:
    """
    Validates the password:
    - 12 to 30 characters
    - Includes lowercase, uppercase, digit, special character
    """
    if not (12 <= len(password) <= 30):
        return False
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,30}$"
    return re.fullmatch(pattern, password) is not None

def validate_zip_code(zip_code: str) -> bool:
    """ Dutch format: 1234AB """
    return re.fullmatch(r"\d{4}[A-Z]{2}", zip_code) is not None

def validate_mobile(phone: str) -> bool:
    """ Must be 8 digits (assumes +31-6 is already included elsewhere) """
    return re.fullmatch(r"\d{8}", phone) is not None

def validate_driving_license(dl: str) -> bool:
    """ Format: XDDDDDDDD or XXDDDDDDD """
    return re.fullmatch(r"[A-Z]{1,2}\d{7,8}", dl) is not None

def validate_age(age: int) -> bool:
    """ Validates age between 1 and 119 """
    return isinstance(age, int) and 0 < age < 120

def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.fullmatch(pattern, email) is not None

def validate_name(name: str) -> bool:
    """ At least 2 characters, letters only """
    return name.isalpha() and len(name) >= 2

def verify_number_input(prompt, min_val, max_val):
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Input must be a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")