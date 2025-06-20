from states.appstate import AppState
from encryption.validators import contains_null_bytes, verify_number_input
import os
import zipfile
from datetime import datetime
from log.manager import LogManager
from uuid import uuid4

class BackupState(AppState):
    BACKUP_DIR = "backups"
    DB_PATH = "UM.db"  
    def __init__(self, context):
        super().__init__(context)
        self.log_manager = LogManager()

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

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"backup_{timestamp}.zip"
        backup_path = os.path.join(self.BACKUP_DIR, backup_name)

        try:
            with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(self.DB_PATH, arcname=os.path.basename(self.DB_PATH))
            print(f"✅ Backup created: {backup_name}")
            self.log_manager.log(self.context.username, "Backup", f"Backup created: {backup_name}")
        except Exception as e:
            print(f"✖ Error creating backup: {e}")
            self.log_manager.log(self.context.username, "Backup", f"Error creating backup: {e}")

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

        # System Admin can only restore the backup with restore code
        if role == "system_admin":
            self._restore_file_with_key()

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
            self.log_manager.log(self.context.username, "Backup", f"Successfully restored backup: {backup_name}")
            return True
        except Exception as e:
            print(f"✖ Error restoring backup: {e}")
            self.log_manager.log(self.context.username, "Backup", f"Error restoring backup: {e}")

    def _restore_file_with_key(self):
        try:
            print("\n🔐 Restore Backup via Restore Code")
            
            # Step 1: Fetch unused restore codes for this user
            encrypted_codes = self.context.admin_repo.get_restorecodes_by_user(self.context.username)
            restorecodes = self.context.admin_repo.decrypt_restorecodes(encrypted_codes)

            # Step 2: Select restore code
            print("Available restore codes:")
            for i, code in enumerate(restorecodes, 1):
                print(f"{i}. {code['code']} for {code['backup_filename']}")
            print("0. Cancel")
            choice = verify_number_input("Select restore code: ", 0, len(restorecodes))
            if choice == 0:
                print("Restore cancelled.")
                return
            selected_code = restorecodes[choice - 1]

            backup_path = os.path.join(self.BACKUP_DIR, selected_code['backup_filename'])

            if not os.path.exists(backup_path):
                print("❌ Backup file not found.")
                self.log_manager.log(self.context.username, "Restore attempt failed", f"File not found: {selected_code['backup_filename']}", suspicious=True)
                return
            
            # before restoring, load existing restore codes
            load_code = self.context.admin_repo.load_restore_code()

            # Step 3: Perform restore 
            success = self._restore_file(selected_code['backup_filename'])

            #reinsert the codes
            if load_code:
                self.context.admin_repo.re_insertcodes(load_code)

            if success:
                # Step 4: Mark restore code as used
                self.context.admin_repo.update_restorecode_used(True, selected_code['id'])
                print("✅ Backup restored successfully.")
                self.log_manager.log(self.context.username, "Backup restored", f"File: {selected_code['backup_filename']}")
            else:
                print("❌ Failed to restore backup.")
                self.log_manager.log(self.context.username, "Restore attempt failed", f"Could not restore {selected_code['backup_filename']}", suspicious=True)

        except Exception as e:
            print(f"An error occurred: {e}")
            self.log_manager.log(self.context.username, "Restore failed", f"Error: {e}", suspicious=True)



