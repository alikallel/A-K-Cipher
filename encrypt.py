from Crypto.Util.number import bytes_to_long
from utils import display_banner

def rsa_encrypt_normal(message, n, e, flag_format=None):
    """Encrypt a message using RSA with normal encryption."""
    if flag_format:
        message = f"{flag_format}{{{message}}}"
    
    # Ensure message is properly converted to bytes
    message_bytes = message.encode('utf-8')
    message_long = bytes_to_long(message_bytes)
    ciphertext = pow(message_long, e, n)
    return ciphertext

def rsa_encrypt_single_prime(message, n, e, flag_format=None):
    """Encrypt a message using RSA with a special case where p = n."""
    if flag_format:
        message = f"{flag_format}{{{message}}}"
    
    # Ensure message is properly converted to bytes
    message_bytes = message.encode('utf-8')
    message_long = bytes_to_long(message_bytes)
    
    # Special case encryption: handling when p = n
    ciphertext = pow(message_long, e, n)
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
        n = int(input("Enter the modulus (n): "))
        e = int(input("Enter the public exponent (e): "))
        p = int(input("Enter the prime p: "))
        
        # Dynamically check if p = n
        if p == n:
            print("Detected p = n, using special encryption method.")
            ciphertext = rsa_encrypt_single_prime(message, n, e, flag_format)
        else:
            print("Using normal encryption method.")
            ciphertext = rsa_encrypt_normal(message, n, e, flag_format)
        
        print(f"\nEncrypted ciphertext: {ciphertext}")
        if flag_format:
            print(f"Original formatted message: {flag_format}{{{message}}}")
    
    except Exception as error:
        print(f"Error during encryption: {error}")
