from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class restoreCode:
    id: Optional[int] = None
    code: str = ""
    backup_filename: str = ""
    used: bool = False
    user_id: int = 0
    generated_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")