import os
from uuid import uuid4
from states.appstate import AppState
from log.manager import LogManager
from encryption.validators import verify_number_input
from models.restorecode import restoreCode
from datetime import datetime

class restoreCodeState(AppState):
    def __init__(self, app):
        super().__init__(app)
        self.log_manager = LogManager()
        self.BACKUP_DIR = "backups"

    def run(self):
        if self.context.role != "super_admin":
            print("You are not authorized to perform this action.")
            self.context.go_back()
            return
        
        print("\n-- Restore Code --")
        print("1. Generate Restore code")
        print("2. Revoke Generated restore code")
        print("0. Exit")
        choice = verify_number_input("Enter your choice: ", 0, 2)

        if choice == 1:
            self._restoreCode()
        elif choice == 2:
            self._revokeRestoreCode()  
        elif choice == 0:
            self.context.go_back()
        else:
            print("Invalid choice. Please try again.")
            self.run()

    def _restoreCode(self):
        try:
            system_admin_id = self.select_systemAdmin()
            if system_admin_id is None:
                print("No system admin selected. Operation cancelled.")
                self.context.go_back()
                return
            backup_filename = self.select_backup()
            if backup_filename is None:
                print("No backup selected. Operation cancelled.")
                self.context.go_back()
                return
            rc = restoreCode(
                code = str(uuid4()),
                backup_filename = backup_filename,
                user_id = system_admin_id
            )
            print("✅ Restore code generated successfully.")
            self.context.admin_repo.add_restorecode(rc)
            self.log_manager.log(self.context.username, f"Restore code genereated", f"Generated for {rc.user_id}")

        except Exception as e:
            print(f"An error occurred: {e}, Incident logged.")
            self.log_manager.log(self.context.username, f"Restore code genereated", f"Failed to generate for {rc.user_id}, Error: {e}", True)
            self.context.go_back()

    def select_systemAdmin(self):
        try:
            users = self.context.admin_repo.get_users_by_role("system_admin")
            print("\nSelect System Admin:")
            for i, user in enumerate(users, 1):
                print(f"{i}. {user[1]}")
            print("0. Exit")
            choice = verify_number_input("Enter your choice: ", 0, len(users))
            if choice == 0:
                self.context.go_back()
                return
            else:
                return users[choice - 1][0]
        except Exception as e:
            print(f"An error occurred: {e}")
            self.context.go_back()
            return    

    def select_backup(self):
        try:
            backups = self.list_backups()
            print("\nSelect Backup:")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup}")
            print("0. Exit")
            choice = verify_number_input("Enter your choice: ", 0, len(backups))
            if choice == 0:
                self.context.go_back()
                return
            else:
                return backups[choice - 1]
        except Exception as e:
            print(f"An error occurred: {e}")
            self.context.go_back()
            return
        
    def list_backups(self):
        if not os.path.exists(self.BACKUP_DIR):
            return []
        return sorted([f for f in os.listdir(self.BACKUP_DIR) if f.endswith(".zip")])
    
    def _revokeRestoreCode(self):
        try:
            encrypted_restore_codes = self.context.admin_repo.get_all_restorecodes_used_is_true()
            decrypted_rc = self.context.admin_repo.decrypt_restorecodes(encrypted_restore_codes)

            if not decrypted_rc:
                print("No restore codes to revoke.")
                return

            print("\nSelect Restore Code to revoke:")
            for i, rc in enumerate(decrypted_rc, 1):
                print(f"{i}. Code: {rc['code']} (User: {rc['username']})")
            print("0. Exit")

            choice = verify_number_input("Enter your choice: ", 0, len(decrypted_rc))
            if choice == 0:
                self.context.go_back()
                return

            selected_rc = decrypted_rc[choice - 1]
            self.context.admin_repo.delete_restorecode(selected_rc["code"])

            print("✅ Restore code revoked successfully.")
            self.log_manager.log(
                self.context.username,
                "Restore code revoked",
                f"Revoked code '{selected_rc['code']}' for user {selected_rc['username']}"
            )

        except Exception as e:
            print(f"An error occurred: {e}, Incident logged.")
            self.log_manager.log(
                self.context.username,
                "Restore code revocation failed",
                f"Error: {e}"
                , True
            )
            self.context.go_back()
