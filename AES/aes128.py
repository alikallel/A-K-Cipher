from Crypto.Cipher import AES
from os import urandom

def pad(data):
    padding_length = 16 - (len(data) % 16)
    return data + bytes([padding_length] * padding_length)


def encrypt_aes_ecb(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext))

def decrypt_aes_ecb(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)

def encrypt_aes_cbc(plaintext, key):
    iv = urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(plaintext))

def decrypt_aes_cbc(ciphertext, key):
    iv, ciphertext = ciphertext[:16], ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(ciphertext)

def aes():
    print("Choose AES Mode:")
    print("1. ECB")
    print("2. CBC")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice not in ["1", "2"]:
        print("Invalid choice. Please select 1 or 2.")
        return

    key = input("Enter a 16-byte encryption key: ").encode()
    print(key)
    if len(key) != 16:
        print("Key must be 16 bytes long.")
        return

    action = input("Choose action (encrypt or decrypt): ").strip().lower()
    if action not in ["encrypt", "decrypt"]:
        print("Invalid action. Please choose 'encrypt' or 'decrypt'.")
        return

    if action == "encrypt":
        plaintext = input("Enter plaintext: ").encode()
        if choice == "1":
            ciphertext = encrypt_aes_ecb(plaintext, key)
        else:
            ciphertext = encrypt_aes_cbc(plaintext, key)
        print(f"Encrypted data (hex): {ciphertext.hex()}")

    elif action == "decrypt":
        ciphertext = bytes.fromhex(input("Enter ciphertext (hex): ").strip())
        if choice == "1":
            try:
                plaintext = decrypt_aes_ecb(ciphertext, key)
            except ValueError:
                print("Decryption failed. Check your key and ciphertext.")
                return
        else:
            try:
                plaintext = decrypt_aes_cbc(ciphertext, key)
            except ValueError:
                print("Decryption failed. Check your key and ciphertext.")
                return

        print(f"Decrypted plaintext: {plaintext}")

