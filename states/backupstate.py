from states.appstate import AppState
from encryption.validators import contains_null_bytes, verify_number_input
import os
import zipfile
from datetime import datetime

class BackupState(AppState):
    BACKUP_DIR = "backups"
    DB_PATH = "UM.db"  

    def run(self):
        while True:
            print("\n--- Backup Management ---")
            print("1. Create Backup")
            print("2. Restore Backup")
            print("0. Go Back")

            choice = verify_number_input("Enter your choice: ", 0, 2)

            if choice == 0:
                self.context.go_back()
                break
            elif choice == 1:
                self.create_backup()
            elif choice == 2:
                self.restore_backup()

    def create_backup(self):
        if not os.path.exists(self.BACKUP_DIR):
            os.makedirs(self.BACKUP_DIR)
    
        if contains_null_bytes(self.DB_PATH):
            print("⚠️ Warning: Database file contains null bytes.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"backup_{timestamp}.zip"
        backup_path = os.path.join(self.BACKUP_DIR, backup_name)

        try:
            with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(self.DB_PATH, arcname=os.path.basename(self.DB_PATH))
            print(f"✅ Backup created: {backup_name}")
        except Exception as e:
            print(f"✖ Error creating backup: {e}")

    def list_backups(self):
        if not os.path.exists(self.BACKUP_DIR):
            return []
        return sorted([f for f in os.listdir(self.BACKUP_DIR) if f.endswith(".zip")])

    def restore_backup(self):
        backups = self.list_backups()
        if not backups:
            print("⚠️ No backups found.")
            return

        role = self.context.role  
        print("\nAvailable backups:")

        # System Admin can only restore the latest backup
        if role == "system_admin":
            latest_backup = backups[-1]
            print(f"1. {latest_backup} (latest backup)")
            print("0. Cancel")
            choice = verify_number_input("Restore this backup? (1 to restore, 0 to cancel): ", 0, 1)
            if choice == 1:
                self._restore_file(latest_backup)
            else:
                print("Restore cancelled.")

        # Super Admin can restore any backup
        elif role == "super_admin":
            for i, b in enumerate(backups, 1):
                print(f"{i}. {b}")
            print("0. Cancel")

            choice = verify_number_input("Select backup to restore: ", 0, len(backups))
            if choice == 0:
                print("Restore cancelled.")
                return
            selected_backup = backups[choice - 1]
            self._restore_file(selected_backup)

        else:
            print("✖ You do not have permission to restore backups.")

    def _restore_file(self, backup_name):
        backup_path = os.path.join(self.BACKUP_DIR, backup_name)
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(path=os.path.dirname(self.DB_PATH))
            print(f"✅ Successfully restored backup: {backup_name}")
        except Exception as e:
            print(f"✖ Error restoring backup: {e}")
