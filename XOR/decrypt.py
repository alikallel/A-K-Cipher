from pwn import xor
from utils import display_banner

def xor_decrypt_normal(ciphertext, key):
    """Decrypt a message using XOR with the given key."""
    # Convert key to bytes if it isn't already
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # If ciphertext is hex string, convert to bytes
    if isinstance(ciphertext, str):
        try:
            ciphertext = bytes.fromhex(ciphertext)
        except ValueError:
            ciphertext = ciphertext.encode('utf-8')
    
    # Perform XOR decryption (same operation as encryption)
    plaintext = xor(ciphertext, key)
    return plaintext

def decrypt_message():
    try:
        print("\nDecryption Input Format:")
        print("1. Raw bytes")
        print("2. Hexadecimal")
        format_choice = input("Choose input format (1-2): ")
        
        if format_choice == "1":
            ciphertext = input("Enter the ciphertext (raw): ").encode('utf-8')
        else:
            ciphertext = input("Enter the ciphertext (hex): ")
        
        key = input("Enter the decryption key: ")
        
        plaintext = xor_decrypt_normal(ciphertext, key)
        
        print(f"\nDecrypted message (utf-8): {plaintext.decode('utf-8', errors='ignore')}")
        print(f"Decrypted message (hex): {plaintext.hex()}")
        print(f"Decrypted message (raw): {plaintext}")
    
    except Exception as error:
        print(f"Error during decryption: {error}")