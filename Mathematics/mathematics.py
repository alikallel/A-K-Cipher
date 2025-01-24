import math
import numpy as np
from sympy import isprime, mod_inverse, discrete_log, factorint
from sympy.ntheory.residue_ntheory import sqrt_mod
from typing import List, Tuple

class MathChallengeSolver:
    def __init__(self):
        self.approaches = {
            1: "Quadratic Residues",
            2: "Modular Square Root",
            3: "Chinese Remainder Theorem",
            4: "Gaussian Reduction",
            5: "Legendre Symbol",
            6: "Number Theory Transformations",
            7: "Tonelli-Shanks Algorithm",
        }
    
    def display_approaches(self):
        print("\nAvailable Mathematical Approaches:")
        for key, approach in self.approaches.items():
            print(f"{key}. {approach}")
    
    def quadratic_residues(self):
        print("\n--- Quadratic Residues ---")
        p = int(input("Enter prime modulus p: "))
        ints = list(map(int, input("Enter quadratic residues (space-separated): ").split()))
        
        ans = [x for x in range(p) if pow(x, 2, p) in ints]
        
        if ans:
            print("Quadratic Residues:", ans)
            print("Minimum Residue:", min(ans))
        else:
            print("No quadratic residues found.")
    
    def modular_square_root(self):
        print("\n--- Modular Square Root ---")
        def legendre(a, p):
            return pow(a, (p - 1) // 2, p)
        
        def tonelli(n, p):
            assert legendre(n, p) == 1, "Not a square (mod p)"
            q = p - 1
            s = 0
            while q % 2 == 0:
                q //= 2
                s += 1
            
            for z in range(2, p):
                if legendre(z, p) == p - 1:
                    break
            
            c = pow(z, q, p)
            r = pow(n, (q + 1) // 2, p)
            t = pow(n, q, p)
            m = s
            
            while t != 1:
                t2 = t
                for i in range(1, m):
                    t2 = (t2 * t2) % p
                    if t2 == 1:
                        break
                
                b = pow(c, 1 << (m - i - 1), p)
                r = (r * b) % p
                c = (b * b) % p
                t = (t * c) % p
                m = i
            
            return r
        
        n = int(input("Enter number to find modular square root: "))
        p = int(input("Enter prime modulus: "))
        
        try:
            root = tonelli(n, p)
            print(f"Modular Square Roots: {root}, {p - root}")
        except AssertionError:
            print("No modular square root exists.")
    
    def chinese_remainder_theorem(self):
        print("\n--- Chinese Remainder Theorem ---")
        a = list(map(int, input("Enter remainders (space-separated): ").split()))
        m = list(map(int, input("Enter moduli (space-separated): ").split()))
        
        def crt(a, m):
            total_mod = math.prod(m)
            result = 0
            for a_i, m_i in zip(a, m):
                p = total_mod // m_i
                result += a_i * p * mod_inverse(p, m_i)
            return result % total_mod
        
        print("Solution:", crt(a, m))
    
    def lattice_reduction(self):
        print("\n--- Lattice Reduction ---")
        def gaussian_reduction(v1: np.ndarray, v2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
            while True:
                if np.dot(v2, v2) < np.dot(v1, v1):
                    v1, v2 = v2, v1
                
                m = round(np.dot(v1, v2) / np.dot(v1, v1))
                if m == 0:
                    return v1, v2
                
                v2 = v2 - m * v1
        
        v1 = np.array(list(map(int, input("Enter first vector (space-separated): ").split())))
        v2 = np.array(list(map(int, input("Enter second vector (space-separated): ").split())))
        
        reduced_v1, reduced_v2 = gaussian_reduction(v1, v2)
        print("Reduced Vector 1:", reduced_v1)
        print("Reduced Vector 2:", reduced_v2)
        print("Dot Product:", np.dot(reduced_v1, reduced_v2))
    
    def legendre_symbol(self):
        print("\n--- Legendre Symbol ---")
        a = int(input("Enter number (a): "))
        p = int(input("Enter prime modulus (p): "))
        
        symbol = pow(a, (p - 1) // 2, p)
        if symbol == 1:
            print(f"(a/p) = 1: {a} is a quadratic residue modulo {p}")
        elif symbol == p - 1:
            print(f"(a/p) = -1: {a} is a quadratic non-residue modulo {p}")
        else:
            print("Invalid input or computation error")
    
    def number_theory_transformations(self):
        print("\n--- Number Theory Transformations ---")
        print("1. Binary to Decimal")
        print("2. Decimal to Binary")
        print("3. Modular Exponentiation")
        
        choice = int(input("Select transformation type: "))
        
        if choice == 1:
            binary = input("Enter binary number: ")
            print("Decimal:", int(binary, 2))
        elif choice == 2:
            decimal = int(input("Enter decimal number: "))
            print("Binary:", bin(decimal)[2:])
        elif choice == 3:
            base = int(input("Enter base: "))
            exponent = int(input("Enter exponent: "))
            modulus = int(input("Enter modulus: "))
            print("Result:", pow(base, exponent, modulus))
    
    def TonelliShanks(self):
        print(" Tonelli-Shanks Algorithm")
        n = int(input("Enter number for square root: "))
        p = int(input("Enter prime modulus: "))
        try:
            root = self.modular_square_root_advanced(n, p)
            print("Square Roots:", root)
        except Exception as e:
            print("Error:", str(e))
       
    def modular_square_root_advanced(self, n, p):
        def legendre(a, p):
            return pow(a, (p - 1) // 2, p)
        
        assert legendre(n, p) == 1, "Not a quadratic residue"
        
        if p % 4 == 3:
            return pow(n, (p + 1) // 4, p)
        
        q = p - 1
        s = 0
        while q % 2 == 0:
            q //= 2
            s += 1
        
        z = 2
        while legendre(z, p) != p - 1:
            z += 1
        
        c = pow(z, q, p)
        r = pow(n, (q + 1) // 2, p)
        t = pow(n, q, p)
        m = s
        
        while t != 1:
            i = 0
            temp = t
            while temp != 1:
                temp = (temp * temp) % p
                i += 1
                if i == m:
                    raise ValueError("No solution")
            
            b = pow(c, 1 << (m - i - 1), p)
            r = (r * b) % p
            t = (t * b * b) % p
            c = (b * b) % p
            m = i
        
        return r
    
    def miller_rabin_test(self, n, k=5):
        if n <= 1 or n == 4:
            return False
        if n <= 3:
            return True
        
        def try_composite(a, d, n, s):
            if pow(a, d, n) == 1:
                return False
            for i in range(s):
                if pow(a, 2**i * d, n) == n - 1:
                    return False
            return True
        
        s = 0
        d = n - 1
        while d % 2 == 0:
            d //= 2
            s += 1
        
        for _ in range(k):
            a = np.random.randint(2, n - 2)
            if try_composite(a, d, n, s):
                return False
        return True
    
    def mathematics(self):
        while True:
            self.display_approaches()
            choice = input("\nSelect an approach (or 'q' to quit): ")
            
            if choice == 'q':
                break
            
            try:
                choice = int(choice)
                methods = {
                    1: self.quadratic_residues,
                    2: self.modular_square_root,
                    3: self.chinese_remainder_theorem,
                    4: self.lattice_reduction,
                    5: self.legendre_symbol,
                    6: self.number_theory_transformations,
                    7: self.TonelliShanks,
                }
                
                if choice in methods:
                    methods[choice]()
                else:
                    print("Invalid approach selected.")
            
            except ValueError:
                print("Invalid input. Please enter a number or 'q'.")
            
            input("\nPress Enter to continue...")
