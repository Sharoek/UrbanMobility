import re
from datetime import datetime
# all validation should be whitelisting, meaning only the characters specified in the regex are allowed
# and everything else is rejected

def validate_username(username: str) -> bool:
    """
    Validates the username:
    - 8 to 10 characters
    - Starts with a letter or underscore
    - Contains only letters, digits, underscores, apostrophes, or periods
    """
    pattern = r"^[a-z_][a-z0-9_.'-]{7,9}$"
    if re.fullmatch(pattern, username, re.IGNORECASE):
        return True
    return False

def validate_password(password: str) -> bool:
    """
    Validates the password:
    - 12 to 30 characters
    - Includes lowercase, uppercase, digit, special character
    """
 
    if (12 <= len(password) <= 30):
        pattern = r"""^
            (?=.*[a-z])                   # at least one lowercase letter
            (?=.*[A-Z])                   # at least one uppercase letter
            (?=.*\d)                      # at least one digit
            (?=.*[~!@#$%&_\+=`|\(){}\[\]:;'<>,.?/])  # at least one special char
            [a-zA-Z0-9~!@#$%&_\+=`|\(){}\[\]:;'<>,.?/]{12,30}  # allowed chars and length
            $"""
        return re.fullmatch(pattern, password, re.VERBOSE) is not None
    return False

def validate_zip_code(zip_code: str) -> bool:
    """ Dutch format: 1234AB """
    if re.fullmatch(r"\d{4}[A-Z]{2}", zip_code) is not None: 
        return True
    return False

def validate_mobile(phone: str) -> bool:
    """ Must be 8 digits (assumes +31-6 is already included elsewhere) """
    if re.fullmatch(r"\d{8}", phone) is not None:
        return True
    return False

def validate_driving_license(dl: str) -> bool:
    """ Format: XDDDDDDDD or XXDDDDDDD """
    if re.fullmatch(r"[A-Z]{1,2}\d{7,8}", dl) is not None:
        return True
    return False

def validate_age(age: int) -> bool:
    """ Validates age between 1 and 119 """
    if isinstance(age, int) and 0 < age < 120:
        return True
    return False

def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.fullmatch(pattern, email) is not None:
        return True
    return False

def validate_name(name: str) -> bool:
    """ At least 2 characters, letters only """
    if name.isalpha() and len(name) >= 2:
        return True
    return False

def verify_number_input(prompt, min_val, max_val, number_type=int):
    while True:
        try:
            value = number_type(input(prompt).strip())
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Input must be a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def validate_and_normalize_coord(coord: float, decimal_places: int = 5) -> float:
    """
    Validates that `coord` has at least `decimal_places` decimals.
    If fewer decimals, raises ValueError.
    If more, truncates to `decimal_places`.
    Always returns a float truncated to `decimal_places`.
    """
    if not isinstance(coord, (int, float)):
        raise ValueError("Coordinate must be a number.")
    
    # Convert to string to check decimal places
    s = f"{coord:.6f}".rstrip('0')  # Up to 6 decimals 
    if '.' not in s:
        # No decimals present
        raise ValueError(f"Coordinate {coord} must have at least {decimal_places} decimals")
    
    decimals = s.split('.')[1]
    if len(decimals) < decimal_places:
        raise ValueError(f"Coordinate {coord} must have at least {decimal_places} decimals")
    
    # Truncate to decimal_places decimals
    factor = 10 ** decimal_places
    truncated = int(coord * factor) / factor
    return truncated


def check_mileage(mileage: float, previous_mileage: float) -> bool:
    """
    Validates that mileage is a non-negative number and not less than previous mileage.
    Args:
        mileage (float): The mileage to validate.
        previous_mileage (float): The previous mileage for comparison.
    """
    if not isinstance(mileage, (int, float)):
        raise ValueError("Mileage must be a number.")
    if mileage < 0:
        raise ValueError("Mileage cannot be negative.")
    if mileage < previous_mileage:
        raise ValueError("Mileage cannot be less than previous mileage.")
     # Check if mileage has more than 2 decimals
    str_mileage = f"{mileage:.10f}"  # represent with enough decimals
    decimals = str_mileage.split(".")[1].rstrip('0')
    if len(decimals) > 2:
        raise ValueError("Mileage can have at most 2 decimal places.")
    if mileage > previous_mileage:
        return True
    return False

def validate_last_maintanence(date: str, previous_date: str) -> bool:
    #enforce YYY-MM-DD
    try:
        # Try to parse the date string strictly with the expected format
        new_dt = datetime.strptime(date, "%Y-%m-%d")
        prev_dt = datetime.strptime(previous_date, "%Y-%m-%d")
        if new_dt > prev_dt:
            return True
        print("The new date cannot be lower than the current date")
        return False
    except ValueError:
        # Raised if the format is wrong or date is invalid (e.g. 2023-02-30)
        print(f"The format provided is wrong: {new_dt}, it needs to be in the fomat YYYY-MM-DD" )
        return False
