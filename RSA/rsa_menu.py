from RSA.encrypt import encrypt_message as rsa_encrypt
from RSA.decrypt import decrypt_message as rsa_decrypt
from RSA.factorize import factorize
from utils.menu_utils import display_table_menu


def rsa_menu():
    while True:
        display_table_menu("RSA Menu", ["Encryption", "Decryption", "Factorization"])
        choice = input("Enter your choice (0-3): ")

        if choice == "1":
            print("\nRSA Encryption Tool")
            rsa_encrypt()
        elif choice == "2":
            print("\nRSA Decryption Tool")
            rsa_decrypt()
        elif choice == "3":
            print("\nRSA Factorization Tool")
            try:
                n = int(input("Enter the RSA modulus (n): "))
                factorize(n)
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        elif choice == "0":
            print("Returning to the main menu...")
            break
        else:
            print("\nInvalid choice. Please select 0-3.")