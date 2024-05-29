# vulnerable_code.py

import os

def insecure_function():
    user_input = input("Enter a filename: ")
    with open(user_input, 'r') as file:
        print(file.read())

def hardcoded_password():
    password = "12345"  # Hardcoded password vulnerability
    print("The password is:", password)

if __name__ == "__main__":
    insecure_function()
    hardcoded_password()

