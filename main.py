from utils.utils import display_banner
from RSA.rsa_menu import rsa_menu
from DiffieHellman.dh_menu import dh_menu
from Caesar.caesar_menu import caesar_menu
from XOR.xor_menu import xor_menu
from AES.aes128 import aes
from Base.base import base
from ROT.rot import rot
from utils.menu_utils import display_table_menu
import sys
from utils.utils import display_banner
from Mathematics.mathematics import MathChallengeSolver

def main():
    display_banner()

    while True:
        display_table_menu(
            "A-K Cipher Tool",
            [
                "RSA",
                "XOR Cipher",
                "Caesar Cipher",
                "AES",
                "Diffie-Hellman",
                "Base Encoding/Decoding",
                "ROT",
                "Mathematics",
            ],
        )

        choice = input("Enter your choice (0-7): ")

        if choice == "1":
            rsa_menu()
        elif choice == "2":
            xor_menu()
        elif choice == "3":
            caesar_menu()
        elif choice == "4":
            aes()
        elif choice == "5":
            dh_menu()
        elif choice == "6":
            base()
        elif choice == "7":
            rot()
        elif choice == "8":
            MathChallengeSolver().mathematics()
        elif choice == "0":
            print("\nThank you for using A-K Cipher Tool! Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please select 0-7.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
