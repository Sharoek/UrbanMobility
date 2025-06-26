import os
import json
from datetime import datetime
from encryption.encryption import encrypt_data, decrypt_data

class LogManager:
    def __init__(self, log_file="logs/activity.log.enc"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def log(self, username, activity, additional_info="", suspicious=False):
        now = datetime.now()
        log_entry = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "username": username,
            "activity": activity,
            "info": additional_info,
            "suspicious": suspicious,
            "read": False
        }
        encrypted_entry = encrypt_data(json.dumps(log_entry)) + "\n"
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(encrypted_entry)

    def read_logs(self):
        logs = []
        if not os.path.exists(self.log_file):
            return logs

        with open(self.log_file, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    decrypted = decrypt_data(line.strip())
                    logs.append(json.loads(decrypted))
                except Exception:
                    continue
        return logs

    def get_unread_suspicious_logs(self):
        return [log for log in self.read_logs() if log["suspicious"] and not log["read"]]

    def mark_logs_as_read(self):
        updated_logs = []
        for log in self.read_logs():
            log["read"] = True
            updated_logs.append(log)

        with open(self.log_file, "w", encoding="utf-8") as file:
            for log in updated_logs:
                encrypted = encrypt_data(json.dumps(log)) + "\n"
                file.write(encrypted)
