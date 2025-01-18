from Crypto.Util.number import inverse, long_to_bytes

def rsa_decrypt_normal(ciphertext, n, e, p, q):
    """Decrypt a ciphertext using RSA with p and q."""
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    plaintext_long = pow(ciphertext, d, n)
    return plaintext_long

def rsa_decrypt_single_prime(ciphertext, n, e):
    """Decrypt a ciphertext using RSA when p = n."""
    q = 1
    phi = (n - 1)
    d = pow(e, -1, phi)
    plaintext_long = pow(ciphertext, d, n)
    return plaintext_long

def decrypt_message():
    try:
        ciphertext = int(input("Enter the ciphertext to decrypt: "))
        e = int(input("Enter the public exponent (e): "))
        p = int(input("Enter the first prime factor (p): "))

        q = None
        n = input("Enter the modulus (n) [leave empty if providing both p and q]: ").strip()
        if not n:
            # If n is not provided, prompt for q
            q = int(input("Enter the second prime factor (q): "))
            n = p * q
        else:
            n = int(n)
        
        if p == n:
            # Special case: p = n
            plaintext_long = rsa_decrypt_single_prime(ciphertext, n, e)
        else:
            # Normal case: need both p and q
            if not q:
                q = int(input("Enter the second prime factor (q): "))
            plaintext_long = rsa_decrypt_normal(ciphertext, n, e, p, q)
        
        plaintext = long_to_bytes(plaintext_long)
        print(f"\nDecrypted plaintext: {plaintext}")
    
    except Exception as error:
        print(f"Error during decryption: {error}")
