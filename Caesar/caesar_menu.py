from Caesar.encrypt import encrypt_message as caesar_encrypt
from Caesar.decrypt import decrypt_message as caesar_decrypt
from utils.menu_utils import display_table_menu

def caesar_menu():
    while True:
        display_table_menu("Caesar Cipher Menu", ["Encryption", "Decryption"])
        choice = input("Enter your choice (0-2): ")

        if choice == "1":
            print("\nCaesar Cipher Encryption Tool")
            caesar_encrypt()
        elif choice == "2":
            print("\nCaesar Cipher Decryption Tool")
            caesar_decrypt()
        elif choice == "0":
            print("Returning to the main menu...")
            break
        else:
            print("\nInvalid choice. Please select 0-2.")