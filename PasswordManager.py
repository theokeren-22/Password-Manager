from cryptography.fernet import Fernet
import os.path


def generate_key():
    return Fernet.generate_key()


def write_key(key):
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    return key


def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password.decode()


def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password.encode())
    return decrypted_password.decode()


def view_passwords(key):
    if not os.path.isfile('passwords.txt'):
        print("No passwords found.")
        return

    with open('passwords.txt', 'r') as file:
        for line in file.readlines():
            data = line.rstrip()
            username, encrypted_password = data.split("|")
            password = decrypt_password(encrypted_password, key)
            print("Username:", username, "| Password:", password)


def add_password(key):
    username = input('Username: ')
    password = input("Password: ")
    encrypted_password = encrypt_password(password, key)

    with open('passwords.txt', 'a') as file:
        file.write(username + "|" + encrypted_password + "\n")


def main():
    if not os.path.isfile("key.key"):
        key = generate_key()
        write_key(key)
    else:
        key = load_key()

    while True:
        mode = input(
            "Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()
        if mode == "q":
            break

        if mode == "view":
            view_passwords(key)
        elif mode == "add":
            add_password(key)
        else:
            print("Invalid mode.")
            continue


if __name__ == '__main__':
    main()
