from utils import display_banner
from encrypt import encrypt_message
from decrypt import decrypt_message
from factorize import factorize
import sys

def print_menu():
    print("\nA-K Cipher Tool for RSA")
    print("----------------------")
    print("1. Encryption")
    print("2. Decryption")
    print("3. Factorization (Find p and q)")
    print("4. Exit")
    print("----------------------")

def main():
    display_banner()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            print("\nRSA Encryption Tool")
            print("-----------------")
            encrypt_message()
        
        elif choice == "2":
            print("\nRSA Decryption Tool")
            print("-----------------")
            decrypt_message()
        
        elif choice == "3":
            print("\nRSA Factorization Tool")
            print("---------------------")
            try:
                n = int(input("Enter the RSA modulus (n): "))
                factorize(n)
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        
        elif choice == "4":
            print("\nThank you for using A-K Cipher Tool!")
            sys.exit(0)
        
        else:
            print("\nInvalid choice. Please select 1, 2, 3, or 4.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
