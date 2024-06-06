import json
import getpass
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()
    
def encrypt_data(key, data):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(key, encrypted_data):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data.encode()).decode()

#Load or create the key
try:
    with open("key.key", "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    key = generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

#Load or create the password database
try:
    with open("passwords.json", "r") as db_file:
        encrypted_db = json.load(db_file)
except FileNotFoundError:
    encrypted_db = {}

while True:
    print("\nPassword Manager Menu:")
    print("1. Add a new password")
    print("2. Retrieve a password")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        website = input("Enter website name: ")
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")

        #Encrypt the password before storing
        encrypted_password = encrypt_data(key, password)
        encrypted_db[website] = {"username": username, "password": encrypted_password}

        with open("passwords.json", "w") as db_file:
            json.dump(encrypted_db, db_file)
        print("Password saved successfully!")

    elif choice == "2":
        website = input("Enter website name: ")
        if website in encrypted_db:
            stored_data = encrypted_db[website]
            decrypted_password = decrypt_data(key, stored_data["password"])
            print(f"Username: {stored_data['username']}")
            print(f"Password: {decrypted_password}")
        else:
            print("Website not found in the database.")

    elif choice == "3":
        print("Exiting Password Manager. Have a great day!")
        break

    else:
        print("Invalid choice. Please select 1, 2, or 3.")
