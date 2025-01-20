from utils.utils import display_banner

def caesar_encrypt_normal(message, shift, flag_format=None):
    if flag_format:
        message = f"{flag_format}{{{message}}}"
    
    encrypted = ""
    for char in message:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            encrypted += chr((ord(char) - base + shift) % 26 + base)
        else:
            encrypted += char
    
    return encrypted

def encrypt_message():
    try:
        print("\nEncryption Options:")
        print("1. Normal message")
        print("2. Flag format (format{message})")
        format_choice = input("Choose format (1-2): ")
        
        flag_format = None
        if format_choice == "2":
            flag_format = input("Enter flag format (e.g., CTF, Alashwas, FLAG): ")
        
        message = input("Enter the message to encrypt: ")
        
        while True:
            try:
                shift = int(input("Enter the shift value (1-25): "))
                if 1 <= shift <= 25:
                    break
                print("Shift must be between 1 and 25.")
            except ValueError:
                print("Please enter a valid number.")
        
        ciphertext = caesar_encrypt_normal(message, shift, flag_format)
        
        print(f"\nEncrypted message: {ciphertext}")
        if flag_format:
            print(f"Original formatted message: {flag_format}{{{message}}}")
        print(f"Shift value used: {shift}")
    
    except Exception as error:
        print(f"Error during encryption: {error}")