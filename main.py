from utils import display_banner
from RSA.encrypt import encrypt_message as rsa_encrypt
from RSA.decrypt import decrypt_message as rsa_decrypt
from XOR.encrypt import encrypt_message as xor_encrypt
from XOR.decrypt import decrypt_message as xor_decrypt
from Caesar.encrypt import encrypt_message as caesar_encrypt
from Caesar.decrypt import decrypt_message as caesar_decrypt
from DiffieHellman.dh_analysis import run_dh_analysis
from RSA.factorize import factorize
from AES.aes128 import aes
import sys

def print_menu():
    print("\nA-K Cipher Tool")
    print("---------------")
    print("1. RSA Encryption")
    print("2. RSA Decryption")
    print("3. RSA Factorization")
    print("4. XOR Encryption")
    print("5. XOR Decryption")
    print("6. Caesar Cipher Encryption")
    print("7. Caesar Cipher Decryption")
    print("8. Diffie-Hellman Analysis")
    print("9. AES")
    print("10. Exit")
    print("---------------")

def main():
    display_banner()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-9): ")
        
        if choice == "1":
            print("\nRSA Encryption Tool")
            print("-----------------")
            rsa_encrypt()
        
        elif choice == "2":
            print("\nRSA Decryption Tool")
            print("-----------------")
            rsa_decrypt()
        
        elif choice == "3":
            print("\nRSA Factorization Tool")
            print("---------------------")
            try:
                n = int(input("Enter the RSA modulus (n): "))
                factorize(n)
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        
        elif choice == "4":
            print("\nXOR Encryption Tool")
            print("-----------------")
            xor_encrypt()
        
        elif choice == "5":
            print("\nXOR Decryption Tool")
            print("-----------------")
            xor_decrypt()
        
        elif choice == "6":
            print("\nCaesar Cipher Encryption Tool")
            print("--------------------------")
            caesar_encrypt()
        
        elif choice == "7":
            print("\nCaesar Cipher Decryption Tool")
            print("--------------------------")
            caesar_decrypt()
        
        elif choice == "8":
            print("\nDiffie-Hellman Key Analysis")
            print("-------------------------")
            run_dh_analysis()
        
        elif choice == "9":
            print("\nThank you for using A-K Cipher Tool!")
            print("--------------------")
            aes()
        elif choice == "10":
            print("\nThank you for using A-K Cipher Tool!")
            sys.exit(0)
            print("--------------------")
            
        else:
            print("\nInvalid choice. Please select 1-10.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()