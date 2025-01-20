from utils.utils import display_banner
from RSA.rsa_menu import rsa_menu
from DiffieHellman.dh_menu import dh_menu
from XOR.encrypt import encrypt_message as xor_encrypt
from XOR.decrypt import decrypt_message as xor_decrypt
from Caesar.caesar_menu import caesar_menu
from AES.aes128 import aes
from utils.menu_utils import display_table_menu
import sys
from utils.utils import display_banner

def main():
    display_banner()

    while True:
        display_table_menu(
            "A-K Cipher Tool",
            [
                "RSA",
                "XOR Encryption",
                "XOR Decryption",
                "Caesar Cipher",
                "AES",
                "Diffie-Hellman",
            ],
        )

        choice = input("Enter your choice (0-6): ")

        if choice == "1":
            rsa_menu()
        elif choice == "2":
            print("\nXOR Encryption Tool")
            xor_encrypt()
        elif choice == "3":
            print("\nXOR Decryption Tool")
            xor_decrypt()
        elif choice == "4":
            caesar_menu()
        elif choice == "5":
            print("\nAES Tool")
            aes()
        elif choice == "6":
            dh_menu()
        elif choice == "0":
            print("\nThank you for using A-K Cipher Tool! Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please select 0-6.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
