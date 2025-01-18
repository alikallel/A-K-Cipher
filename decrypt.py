from Crypto.Util.number import inverse, long_to_bytes
from utils import display_banner

def rsa_decrypt_normal(ciphertext, n, e, p, q):
    """Decrypt a ciphertext using RSA with p and q."""
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    plaintext_long = pow(ciphertext, d, n)
    return plaintext_long

def rsa_decrypt_signle_prime(ciphertext, n, e):
    """Decrypt a ciphertext using RSA when p = n."""
    q = 1
    phi = (n - 1)
    d = pow(e, -1, phi)
    plaintext_long = pow(ciphertext, d, n)
    return plaintext_long

def decrypt_message():
    try:
        ciphertext = int(input("Enter the ciphertext to decrypt: "))
        n = int(input("Enter the modulus (n): "))
        e = int(input("Enter the public exponent (e): "))
        p = int(input("Enter the first prime factor (p):  "))
        
        if p == n:
            # Special case: p = n
            plaintext_long = rsa_decrypt_signle_prime(ciphertext, n, e)
        else:
            # Normal case: need both p and q
            q = int(input("Enter the second prime factor (q): "))
            plaintext_long = rsa_decrypt_normal(ciphertext, n, e, p, q)
        
        plaintext = long_to_bytes(plaintext_long)
        print(f"\nDecrypted plaintext: {plaintext}")
    
    except Exception as error:
        print(f"Error during decryption: {error}")
