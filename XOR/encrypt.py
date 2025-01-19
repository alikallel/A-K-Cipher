from pwn import xor
from utils import display_banner

def xor_encrypt_normal(message, key, flag_format=None):
    """Encrypt a message using XOR with the given key."""
    if flag_format:
        message = f"{flag_format}{{{message}}}"
    
    # Convert message and key to bytes if they aren't already
    if isinstance(message, str):
        message = message.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # Perform XOR encryption
    ciphertext = xor(message, key)
    return ciphertext

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
        key = input("Enter the encryption key: ")
        
        ciphertext = xor_encrypt_normal(message, key, flag_format)
        
        print(f"\nEncrypted ciphertext (hex): {ciphertext.hex()}")
        print(f"Encrypted ciphertext (raw): {ciphertext}")
        if flag_format:
            print(f"Original formatted message: {flag_format}{{{message}}}")
    
    except Exception as error:
        print(f"Error during encryption: {error}")