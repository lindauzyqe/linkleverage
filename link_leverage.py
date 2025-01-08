import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

class LinkLeverage:
    def __init__(self):
        self.associations_file = Path('associations.json')
        self.shortcuts_dir = Path('shortcuts')

    def create_association(self, extension, program_path):
        associations = self.load_associations()
        associations[extension] = program_path
        self.save_associations(associations)
        print(f"Association created: {extension} -> {program_path}")

    def remove_association(self, extension):
        associations = self.load_associations()
        if extension in associations:
            del associations[extension]
            self.save_associations(associations)
            print(f"Association removed for extension: {extension}")
        else:
            print(f"No association found for extension: {extension}")

    def list_associations(self):
        associations = self.load_associations()
        if not associations:
            print("No associations found.")
        else:
            for ext, prog in associations.items():
                print(f"{ext} -> {prog}")

    def create_shortcut(self, target_path):
        if not self.shortcuts_dir.exists():
            self.shortcuts_dir.mkdir()
        
        shortcut_name = Path(target_path).stem + '.lnk'
        shortcut_path = self.shortcuts_dir / shortcut_name
        
        if sys.platform == "win32":
            try:
                subprocess.run(['mklink', shortcut_path, target_path], shell=True, check=True)
                print(f"Shortcut created: {shortcut_path}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to create shortcut: {str(e)}")
        else:
            print("This feature is only supported on Windows.")

    def load_associations(self):
        if self.associations_file.exists():
            with open(self.associations_file, 'r') as file:
                return json.load(file)
        return {}

    def save_associations(self, associations):
        with open(self.associations_file, 'w') as file:
            json.dump(associations, file, indent=4)

def main():
    ll = LinkLeverage()
    print("Welcome to LinkLeverage!")
    while True:
        print("\nOptions:")
        print("1. Create association")
        print("2. Remove association")
        print("3. List associations")
        print("4. Create shortcut")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            ext = input("Enter file extension (e.g., .txt): ")
            prog = input("Enter the program path: ")
            ll.create_association(ext, prog)
        elif choice == '2':
            ext = input("Enter file extension to remove: ")
            ll.remove_association(ext)
        elif choice == '3':
            ll.list_associations()
        elif choice == '4':
            target = input("Enter the full path of the file to create a shortcut: ")
            ll.create_shortcut(target)
        elif choice == '5':
            print("Exiting LinkLeverage.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()