from Crypto.Util.number import inverse, long_to_bytes
from math import isqrt
from typing import Optional, Tuple

class RSACracker:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def _print(self, msg: str):
        if self.verbose:
            print(msg)

    def factorize_fermat(self, n: int) :
      
        self._print("Attempting Fermat factorization...")
        a = isqrt(n)
        b2 = a*a - n
        b = isqrt(n)
        count = 0
        while b*b != b2 and count < 1000:
            a = a + 1
            b2 = a*a - n
            b = isqrt(b2)
            count += 1
        if b*b == b2:
            p = a + b
            q = a - b
            if p * q == n:
                return p, q
        return None

    def common_modulus_attack(self, c1: int, c2: int, e1: int, e2: int, n: int) -> Optional[bytes]:
        
        self._print("Attempting common modulus attack...")
        
        # Calculate coefficients using extended GCD
        def extended_gcd(a: int, b: int):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y

        # Get GCD and coefficients
        gcd, a, b = extended_gcd(e1, e2)
        
        if gcd != 1:
            self._print("Common modulus attack failed: GCD(e1,e2) != 1")
            return None

        # Handle negative coefficients
        if b < 0:
            b = -b
            c2 = inverse(c2, n)
        if a < 0:
            a = -a
            c1 = inverse(c1, n)

        # Calculate message using Chinese Remainder Theorem
        m = (pow(c1, a, n) * pow(c2, b, n)) % n
        
        try:
            return long_to_bytes(m)
        except Exception:
            self._print("Failed to convert result to bytes")
            return None


    def wiener_attack(self, e: int, n: int) :
        """
        Wiener's attack for small private exponent.
        Works when d < (1/3) * N^(1/4)
        """
        
        return None

    def decrypt_message(self, ciphertext: int, n: int, e: int, p: Optional[int] = None,
                        q: Optional[int] = None, d: Optional[int] = None) -> Optional[bytes]:
        
        try:
            if p==n :
                q = 1
                phi = (n - 1)
                d = pow(e, -1, phi)
                plaintext_long = pow(ciphertext, d, n)
                return long_to_bytes(plaintext_long)

            if p and q:
                phi = (p - 1) * (q - 1)
                d = inverse(e, phi)
                plaintext = pow(ciphertext, d, n)
                return long_to_bytes(plaintext)

            if d:
                plaintext = pow(ciphertext, d, n)
                return long_to_bytes(plaintext)

            factors = self.factorize_fermat(n)
            if factors:
                p, q = factors
                self._print(f"Fermat factorization successful: p = {p}, q = {q}")
                return self.decrypt_message(ciphertext, n, e, p, q)

            self._print("All attacks failed.")
            return None

        except Exception as error:
            self._print(f"Error during decryption: {error}")
            return None


def decrypt_message():
    cracker = RSACracker()
    try:
        mode = input("Choose decryption method: (1) Single ciphertext, (2) Common Modulus Attack: ").strip()

        if mode == "1":
            ciphertext = int(input("Enter the ciphertext to decrypt: "))
            n = input("Enter the modulus (n): ").strip()
            e = int(input("Enter the public exponent (e): "))

            p = input("Enter the first prime factor (p) if known [press Enter to skip]: ").strip()
            if (p != n):
                q = input("Enter the second prime factor (q) if known [press Enter to skip]: ").strip()
            else:
                q= None

            p = int(p) if p else None
            q = int(q) if q else None
            
            if not n and p and q:
                n = p * q
            elif n:
                n = int(n)
            else:
                n = None
                
            if not n:
                print("Error: Must provide either n or both p and q")
                return

            result = cracker.decrypt_message(ciphertext, n, e, p, q)
            if result:
                print(f"\nDecrypted plaintext: {result}")
            else:
                print("\nDecryption failed. Try with different parameters or attack methods.")

        elif mode == "2":
            c1 = int(input("Enter the first ciphertext (c1): "))
            c2 = int(input("Enter the second ciphertext (c2): "))
            e1 = int(input("Enter the first public exponent (e1): "))
            e2 = int(input("Enter the second public exponent (e2): "))
            n = int(input("Enter the modulus (n): "))

            result = cracker.common_modulus_attack(c1, c2, e1, e2, n)
            if result:
                print(f"\nDecrypted plaintext: {result}")
            else:
                print("\nCommon Modulus Attack failed. Ensure inputs are correct and gcd(e1, e2) = 1.")

        else:
            print("Invalid option. Choose either 1 or 2.")

    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except Exception as error:
        print(f"Error: {error}")
