from XOR.encrypt import encrypt_message as xor_encrypt
from XOR.decrypt import decrypt_message as xor_decrypt
from utils.menu_utils import display_table_menu

def xor_menu():
    while True:
        display_table_menu("XOR Cipher Menu", ["Encryption", "Decryption"])
        choice = input("Enter your choice (0-2): ")

        if choice == "1":
            print("\nXOR Encryption Tool")
            xor_encrypt()
        elif choice == "2":
            print("\nXOR Decryption Tool")
            xor_decrypt()
        elif choice == "0":
            print("Returning to the main menu...")
            break
        else:
            print("\nInvalid choice. Please select 0-2.")