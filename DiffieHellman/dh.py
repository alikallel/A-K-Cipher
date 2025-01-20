from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    
    try:
        return unpad(plaintext, 16).decode('ascii')
    except:
        return plaintext.decode('ascii')

def find_generator(p):
    for k in range(2, p):
        is_generator = True
        for n in range(2, p):
            if pow(k, n, p) == k:
                is_generator = False
                break
        if is_generator:
            return k
    return None

def calculate_shared_secret(base, exponent, modulus):
    return pow(base, exponent, modulus)

def decrypt_direct(A, b, p, iv, encrypted_flag):
    shared_secret = pow(A, b, p)
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    ct = bytes.fromhex(encrypted_flag)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    flag = cipher.decrypt(ct)
    return flag

def diffiehellman():
    while True:
        print("\nDiffie-Hellman Problem Solver")
        print("1. Find Generator")
        print("2. Calculate Modular Exponentiation (g^a mod p)")
        print("3. Calculate Shared Secret")
        print("4. Decrypt Message using Shared Secret")
        print("5. Decrypt Message using Direct Parameters")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            p = int(input("Enter the prime modulus (p): "))
            generator = find_generator(p)
            if generator:
                print(f"First generator found: {generator}")
            else:
                print("No generator found")
                
        elif choice == '2':
            g = int(input("Enter base (g): "))
            a = int(input("Enter exponent (a): "))
            p = int(input("Enter modulus (p): "))
            result = pow(g, a, p)
            print(f"Result: {result}")
            
        elif choice == '3':
            print("\nCalculating shared secret (A^b mod p)")
            A = int(input("Enter public value (A): "))
            b = int(input("Enter private exponent (b): "))
            p = int(input("Enter modulus (p): "))
            shared_secret = calculate_shared_secret(A, b, p)
            print(f"Shared Secret: {shared_secret}")
            
        elif choice == '4':
            shared_secret = int(input("Enter shared secret: "))
            iv = input("Enter IV (hex): ")
            ciphertext = input("Enter encrypted flag (hex): ")
            
            try:
                decrypted = decrypt_flag(shared_secret, iv, ciphertext)
                print(f"Decrypted flag: {decrypted}")
            except Exception as e:
                print(f"Error decrypting: {e}")
        elif choice == '5':
            print("\nDecrypting flag using direct parameters")
            A = int(input("Enter public value (A): "))
            b = int(input("Enter private exponent (b): "))
            p = int(input("Enter modulus (p): "))
            iv = input("Enter IV (hex): ")
            encrypted_flag = input("Enter encrypted flag (hex): ")
            
            try:
                flag = decrypt_direct(A, b, p, iv, encrypted_flag)
                print(f"Decrypted flag: {flag}")
            except Exception as e:
                print(f"Error decrypting: {e}")        
        elif choice == '6':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

