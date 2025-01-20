from utils.utils import display_banner

def caesar_decrypt_normal(ciphertext, shift):

    decrypted = ""
    for char in ciphertext:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            decrypted += chr((ord(char) - base - shift) % 26 + base)
        else:
            decrypted += char
    
    return decrypted

def decrypt_message():
    try:
        print("\nDecryption Options:")
        print("1. Known shift")
        print("2. Brute force (try all shifts)")
        decrypt_choice = input("Choose option (1-2): ")
        
        ciphertext = input("Enter the encrypted message: ")
        
        if decrypt_choice == "1":
            while True:
                try:
                    shift = int(input("Enter the shift value (1-25): "))
                    if 1 <= shift <= 25:
                        break
                    print("Shift must be between 1 and 25.")
                except ValueError:
                    print("Please enter a valid number.")
            
            plaintext = caesar_decrypt_normal(ciphertext, shift)
            print(f"\nDecrypted message: {plaintext}")
            print(f"Shift value used: {shift}")
        
        else:
            print("\nAll possible decryptions:")
            print("-" * 40)
            for shift in range(1, 26):
                plaintext = caesar_decrypt_normal(ciphertext, shift)
                print(f"Shift {shift:2d}: {plaintext}")
            print("-" * 40)
    
    except Exception as error:
        print(f"Error during decryption: {error}")