from typing import Optional, Tuple, List, Dict
import sympy
from math import gcd
import logging
from tqdm import tqdm

class DHExploiter:
    def __init__(self, p: int, g: Optional[int] = None, 
                 public_A: Optional[int] = None, 
                 public_B: Optional[int] = None,
                 debug: bool = False):
        self.p = p
        self.g = g
        self.public_A = public_A 
        self.public_B = public_B
        self.logger = self._setup_logging(debug)
        
    def _setup_logging(self, debug: bool) -> logging.Logger:
        logger = logging.getLogger('DHExploiter')
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def check_vulnerabilities(self) -> Dict:
        vulnerabilities = {
            "weak_prime": False,
            "small_subgroup": False,
            "non_safe_prime": False,
            "weak_generator": False,
            "composite_modulus": False,
            "small_factors": [],
            "special_number": False,
            "pohlig_hellman_vulnerable": False,
            "risk_level": "LOW",
            "explanation": []
        }
        
        if not sympy.isprime(self.p):
            vulnerabilities["composite_modulus"] = True
            vulnerabilities["risk_level"] = "CRITICAL"
            vulnerabilities["explanation"].append(f"CRITICAL: Modulus {self.p} is not prime!")
            return vulnerabilities

        if self.p.bit_length() < 2048:
            vulnerabilities["weak_prime"] = True
            vulnerabilities["risk_level"] = "HIGH"
            vulnerabilities["explanation"].append(
                f"HIGH RISK: Prime size ({self.p.bit_length()} bits) is less than 2048 bits"
            )

        if self.is_special_form_number():
            vulnerabilities["special_number"] = True
            vulnerabilities["risk_level"] = "HIGH"
            vulnerabilities["explanation"].append(
                "HIGH RISK: Prime appears to be in a special form vulnerable to SNFS"
            )

        factors = self.get_prime_factors(self.p - 1)
        small_factors = [(p, e) for p, e in factors if p < 2**16]
        
        if small_factors:
            vulnerabilities["small_factors"] = small_factors
            vulnerabilities["risk_level"] = "HIGH"
            vulnerabilities["explanation"].append(
                f"HIGH RISK: Found small factors in p-1: {small_factors}"
            )

        if not self.is_safe_prime():
            vulnerabilities["non_safe_prime"] = True
            if vulnerabilities["risk_level"] != "HIGH":
                vulnerabilities["risk_level"] = "MEDIUM"
            vulnerabilities["explanation"].append(
                "MEDIUM RISK: p is not a safe prime"
            )

        if self.g is not None:
            if self.g <= 1 or self.g >= self.p:
                vulnerabilities["weak_generator"] = True
                vulnerabilities["explanation"].append(
                    "HIGH RISK: Generator out of valid range"
                )
                vulnerabilities["risk_level"] = "HIGH"

        return vulnerabilities

    def print_results(self):
        print("\nAnalyzing DH parameters for vulnerabilities...")
        vulns = self.check_vulnerabilities()
        
        print("\nVulnerability Analysis Results:")
        print("-" * 40)
        print(f"Risk Level: {vulns['risk_level']}")
        
        for exp in vulns['explanation']:
            print(f"- {exp}")
            
        if vulns['small_factors']:
            print(f"\nSmall factors found in p-1:")
            for prime, power in vulns['small_factors']:
                print(f"- Prime: {prime}, Power: {power}")
            
        if vulns['risk_level'] in ['HIGH', 'CRITICAL']:
            print("\nAttempting key recovery...")
            results = self.attempt_key_recovery()
            
            if results['success']:
                print(f"\nKey recovered successfully!")
                print(f"Method used: {results['method_used']}")
                print(f"Private key: {results['private_key']}")
                if results.get('shared_secret'):
                    print(f"Shared secret: {results['shared_secret']}")
            else:
                print("\nUnable to recover key with current methods")
                if 'error' in results:
                    print(f"Error: {results['error']}")
                if 'method_suggestion' in results:
                    print(f"Suggested method: {results['method_suggestion']}")

    def is_special_form_number(self) -> bool:
        # Check if p is close to a power of 2
        closest_power_2 = 2 ** (self.p.bit_length() - 1)
        if abs(self.p - closest_power_2) < 2**20:
            return True
            
        # Check if p is of form 2^n ± 1
        n = self.p.bit_length()
        if abs(self.p - (2**n - 1)) < 1000 or abs(self.p - (2**n + 1)) < 1000:
            return True
            
        return False

    def is_safe_prime(self) -> bool:
        q = (self.p - 1) // 2
        return sympy.isprime(q)

    def get_prime_factors(self, n: int) -> List[Tuple[int, int]]:
        factors = []
        for prime in sympy.primefactors(n):
            power = 0
            temp_n = n
            while temp_n % prime == 0:
                power += 1
                temp_n //= prime
            factors.append((prime, power))
        return sorted(factors)

    def attempt_key_recovery(self) -> Dict:
        results = {
            "success": False,
            "private_key": None,
            "method_used": None,
            "shared_secret": None
        }
        
        if not all([self.g, self.public_A or self.public_B]):
            return {
                "success": False,
                "error": "Insufficient parameters for key recovery"
            }
            
        target = self.public_A if self.public_A is not None else self.public_B
        
        order = self.find_element_order(self.g)
        if order < 2**32:
            self.logger.info("Attempting small subgroup attack...")
            key = self.small_subgroup_attack(target, order)
            if key is not None:
                results.update({
                    "success": True,
                    "private_key": key,
                    "method_used": "small_subgroup"
                })
                return results

        return results

    def find_element_order(self, element: int) -> int:
        if gcd(element, self.p) != 1:
            return 0
            
        factors = self.get_prime_factors(self.p - 1)
        order = self.p - 1
        
        for prime, exp in factors:
            temp_order = order
            while temp_order > 1:
                if pow(element, temp_order // prime, self.p) != 1:
                    break
                temp_order //= prime
            order = temp_order
            
        return order

    def small_subgroup_attack(self, target: int, order: int) -> Optional[int]:
        for i in tqdm(range(order), desc="Trying small subgroup values"):
            if pow(self.g, i, self.p) == target:
                return i
        return None

def run_dh_analysis():
    try:
        print("Diffie-Hellman Parameter Analyzer")
        print("-" * 40)
        
        while True:
            try:
                p = int(input("Enter prime modulus (p): ").strip())
                if p > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        g_input = input("Enter generator (g) [Enter to skip]: ").strip()
        g = int(g_input) if g_input else None
        
        A_input = input("Enter public value A [Enter to skip]: ").strip()
        public_A = int(A_input) if A_input else None
        
        B_input = input("Enter public value B [Enter to skip]: ").strip()
        public_B = int(B_input) if B_input else None
        
        debug = input("Enable debug logging? (y/N): ").lower().startswith('y')
        
        exploiter = DHExploiter(p, g, public_A, public_B, debug)
        exploiter.print_results()
        
    except KeyboardInterrupt:
        print("\nAnalysis cancelled by user.")
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")