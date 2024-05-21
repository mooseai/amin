from cryptography.fernet import Fernet
import os
import random
import string

class PasswordManager:
    def __init__(self, key_file="key.key", data_file="passwords.txt"):
        self.key_file = key_file
        self.data_file = data_file
        self.load_or_create_key()
        self.locked = True
        self.unlock()

    def load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(self.key)

    def encrypt(self, data):
        cipher_suite = Fernet(self.key)
        return cipher_suite.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        cipher_suite = Fernet(self.key)
        return cipher_suite.decrypt(encrypted_data).decode()

    def save_password(self, service, username, password):
        with open(self.data_file, 'a') as f:
            encrypted_data = self.encrypt(f"{service},{username},{password}\n")
            f.write(encrypted_data.decode())

    def retrieve_passwords(self):
        passwords = []
        with open(self.data_file, 'rb') as f:
            for line in f:
                decrypted_line = self.decrypt(line)
                service, username, password = decrypted_line.strip().split(',')
                passwords.append((service, username, password))
        return passwords

    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    def unlock(self):
        while self.locked:
            password_attempt = input("Enter the password to unlock: ")
            if password_attempt == "ghawassa":  # Change "ghawassa" to your desired password
                self.locked = False
                print("Access Granted.")
            else:
                print("Incorrect password. Try again.")

if __name__ == "__main__":
    password_manager = PasswordManager()

    while not password_manager.locked:
        print("\n1. Save Password")
        print("2. Retrieve Passwords")
        print("3. Generate Password")
        print("4. Lock App")

        choice = input("Enter your choice: ")

        if choice == '1':
            service = input("Enter the service: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            password_manager.save_password(service, username, password)
            print("Password saved successfully!")
        elif choice == '2':
            passwords = password_manager.retrieve_passwords()
            if passwords:
                service_to_retrieve = input("Enter the service: ")
                found = False
                for service, username, password in passwords:
                    if service == service_to_retrieve:
                        found = True
                        print(f"Service: {service}, Username: {username}, Password: {password}")
                if not found:
                    print("No passwords saved for this service.")
            else:
                print("No passwords saved yet.")
        elif choice == '3':
            service = input("Enter the service: ")
            length = int(input("Enter the length of the password: "))
            generated_password = password_manager.generate_password(length)
            print(f"Generated Password for {service}: {generated_password}")
        elif choice == '4':
            password_manager.locked = True
            print("App locked.")
        else:
            print("Invalid choice. Please try again.")