from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Profile:
    first_name: str
    last_name: str
    registration_date: datetime = field(default_factory=datetime.now)
