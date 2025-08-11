import tkinter as tk
from tkinter import ttk
import math
import numpy as np
from sympy import isprime, mod_inverse, discrete_log, factorint
from sympy.ntheory.residue_ntheory import sqrt_mod
from gui.base_module import BaseGUIModule


class MathModule(BaseGUIModule):
    def __init__(self, parent, main_window=None):
        super().__init__(parent, "Mathematical Tools")
        self.main_window = main_window

    def init_module(self):
        # Create multiple tabs for different mathematical operations
        self.quadratic_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.quadratic_frame, text="Quadratic Residues")
        self.create_quadratic_tab()

        self.modular_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.modular_frame, text="Modular Operations")
        self.create_modular_tab()

        self.crt_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.crt_frame, text="Chinese Remainder")
        self.create_crt_tab()

        self.lattice_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.lattice_frame, text="Lattice Reduction")
        self.create_lattice_tab()

        self.transforms_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.transforms_frame, text="Transformations")
        self.create_transforms_tab()

    def create_quadratic_tab(self):
        """Tab for quadratic residues and Legendre symbol"""
        input_frame = self.create_input_frame(self.quadratic_frame, "Quadratic Residues & Legendre Symbol")
        
        # Operation selection
        operation_frame = ttk.Frame(input_frame, style='Main.TFrame')
        operation_frame.pack(fill='x')
        ttk.Label(operation_frame, text="Operation:", style='Info.TLabel').pack(anchor='w')
        self.quad_operation = ttk.Combobox(operation_frame, values=[
            "Find Quadratic Residues",
            "Legendre Symbol",
            "Check Quadratic Residue"
        ], state='readonly')
        self.quad_operation.set("Find Quadratic Residues")
        self.quad_operation.pack(fill='x', pady=(0, 10))
        self.quad_operation.bind('<<ComboboxSelected>>', self.on_quad_operation_change)

        # Parameters frame
        params_frame = ttk.Frame(input_frame, style='Main.TFrame')
        params_frame.pack(fill='x', pady=(0, 10))

        left_frame = ttk.Frame(params_frame, style='Main.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.quad_prime = self.create_text_input(left_frame, "Prime modulus (p):")
        
        right_frame = ttk.Frame(params_frame, style='Main.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        self.quad_number = self.create_text_input(right_frame, "Number (a):")

        # Container for dynamic content (ensures proper positioning)
        self.quad_dynamic_container = ttk.Frame(input_frame, style='Main.TFrame')
        self.quad_dynamic_container.pack(fill='x', pady=(0, 10))

        # Residues input (for finding quadratic residues) - now in dynamic container
        self.residues_frame = ttk.Frame(self.quad_dynamic_container, style='Main.TFrame')
        self.quad_residues = self.create_text_input(self.residues_frame, "Quadratic Residues (space-separated):")

        # Buttons (placed after dynamic container)
        button_frame = self.create_button_frame(input_frame)
        self.create_action_button(button_frame, "Calculate", self.perform_quadratic, 0)
        self.create_action_button(button_frame, "Clear", self.clear_quadratic, 1)
        self.create_return_button(button_frame, self._return_to_main)

        # Output
        output_frame = self.create_output_frame(self.quadratic_frame, "Results")
        self.quad_output = self.create_output_text(output_frame)

        # Set initial visibility
        self.on_quad_operation_change()

    def create_modular_tab(self):
        """Tab for modular square roots and Tonelli-Shanks"""
        input_frame = self.create_input_frame(self.modular_frame, "Modular Operations")
        
        # Operation selection
        operation_frame = ttk.Frame(input_frame, style='Main.TFrame')
        operation_frame.pack(fill='x')
        ttk.Label(operation_frame, text="Operation:", style='Info.TLabel').pack(anchor='w')
        self.mod_operation = ttk.Combobox(operation_frame, values=[
            "Modular Square Root",
            "Modular Exponentiation",
            "Modular Inverse",
            "Discrete Logarithm"
        ], state='readonly')
        self.mod_operation.set("Modular Square Root")
        self.mod_operation.pack(fill='x', pady=(0, 10))
        self.mod_operation.bind('<<ComboboxSelected>>', self.on_mod_operation_change)

        # Parameters frame
        params_frame = ttk.Frame(input_frame, style='Main.TFrame')
        params_frame.pack(fill='x', pady=(0, 10))

        left_frame = ttk.Frame(params_frame, style='Main.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.mod_number = self.create_text_input(left_frame, "Number:")
        self.mod_exponent = self.create_text_input(left_frame, "Exponent:")
        
        right_frame = ttk.Frame(params_frame, style='Main.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        self.mod_prime = self.create_text_input(right_frame, "Prime modulus:")
        self.mod_base = self.create_text_input(right_frame, "Base:")

        # Container for dynamic content (for field visibility changes)
        self.mod_dynamic_container = ttk.Frame(input_frame, style='Main.TFrame')
        self.mod_dynamic_container.pack(fill='x', pady=(0, 10))

        # Buttons (placed after dynamic container)
        button_frame = self.create_button_frame(input_frame)
        self.create_action_button(button_frame, "Calculate", self.perform_modular, 0)
        self.create_action_button(button_frame, "Clear", self.clear_modular, 1)
        self.create_return_button(button_frame, self._return_to_main)

        # Output
        output_frame = self.create_output_frame(self.modular_frame, "Results")
        self.mod_output = self.create_output_text(output_frame)

        # Set initial field visibility
        self.on_mod_operation_change()

    def create_crt_tab(self):
        """Tab for Chinese Remainder Theorem"""
        input_frame = self.create_input_frame(self.crt_frame, "Chinese Remainder Theorem")
        
        # Instructions
        info_label = ttk.Label(input_frame, 
                              text="Enter remainders and moduli as space-separated values",
                              style='Info.TLabel')
        info_label.pack(pady=(0, 10))

        # Parameters
        self.crt_remainders = self.create_text_input(input_frame, "Remainders (space-separated):")
        self.crt_moduli = self.create_text_input(input_frame, "Moduli (space-separated):")

        # Container for any potential dynamic content
        self.crt_dynamic_container = ttk.Frame(input_frame, style='Main.TFrame')
        self.crt_dynamic_container.pack(fill='x', pady=(0, 10))

        # Buttons
        button_frame = self.create_button_frame(input_frame)
        self.create_action_button(button_frame, "Solve CRT", self.perform_crt, 0)
        self.create_action_button(button_frame, "Clear", self.clear_crt, 1)
        self.create_return_button(button_frame, self._return_to_main)

        # Output
        output_frame = self.create_output_frame(self.crt_frame, "CRT Solution")
        self.crt_output = self.create_output_text(output_frame)

    def create_lattice_tab(self):
        """Tab for Lattice Reduction (Gaussian)"""
        input_frame = self.create_input_frame(self.lattice_frame, "Lattice Reduction")
        
        # Instructions
        info_label = ttk.Label(input_frame, 
                              text="Enter vectors as space-separated coordinates",
                              style='Info.TLabel')
        info_label.pack(pady=(0, 10))

        # Parameters
        self.lattice_v1 = self.create_text_input(input_frame, "Vector 1 (space-separated):")
        self.lattice_v2 = self.create_text_input(input_frame, "Vector 2 (space-separated):")

        # Container for any potential dynamic content
        self.lattice_dynamic_container = ttk.Frame(input_frame, style='Main.TFrame')
        self.lattice_dynamic_container.pack(fill='x', pady=(0, 10))

        # Buttons
        button_frame = self.create_button_frame(input_frame)
        self.create_action_button(button_frame, "Reduce", self.perform_lattice, 0)
        self.create_action_button(button_frame, "Clear", self.clear_lattice, 1)
        self.create_return_button(button_frame, self._return_to_main)

        # Output
        output_frame = self.create_output_frame(self.lattice_frame, "Reduced Vectors")
        self.lattice_output = self.create_output_text(output_frame)

    def create_transforms_tab(self):
        """Tab for number theory transformations"""
        input_frame = self.create_input_frame(self.transforms_frame, "Number Theory Transformations")
        
        # Operation selection
        operation_frame = ttk.Frame(input_frame, style='Main.TFrame')
        operation_frame.pack(fill='x')
        ttk.Label(operation_frame, text="Operation:", style='Info.TLabel').pack(anchor='w')
        self.trans_operation = ttk.Combobox(operation_frame, values=[
            "Binary to Decimal",
            "Decimal to Binary",
            "Decimal to Hex",
            "Hex to Decimal",
            "Prime Factorization",
            "Primality Test"
        ], state='readonly')
        self.trans_operation.set("Binary to Decimal")
        self.trans_operation.pack(fill='x', pady=(0, 10))

        # Input
        self.trans_input = self.create_text_input(input_frame, "Input:")

        # Container for any potential dynamic content
        self.trans_dynamic_container = ttk.Frame(input_frame, style='Main.TFrame')
        self.trans_dynamic_container.pack(fill='x', pady=(0, 10))

        # Buttons
        button_frame = self.create_button_frame(input_frame)
        self.create_action_button(button_frame, "Transform", self.perform_transform, 0)
        self.create_action_button(button_frame, "Clear", self.clear_transform, 1)
        self.create_return_button(button_frame, self._return_to_main)

        # Output
        output_frame = self.create_output_frame(self.transforms_frame, "Transformation Result")
        self.trans_output = self.create_output_text(output_frame)

    def on_quad_operation_change(self, event=None):
        """Show/hide fields based on quadratic operation"""
        operation = self.quad_operation.get()
        if operation == "Find Quadratic Residues":
            self.residues_frame.pack(fill='x', pady=(0, 10))
            # Hide number input for this operation
            self.quad_number.master.pack_forget()
        else:
            self.residues_frame.pack_forget()
            # Show number input for Legendre symbol and residue check
            self.quad_number.master.pack(side='right', fill='both', expand=True, padx=(5, 0))

    def on_mod_operation_change(self, event=None):
        """Adjust field visibility based on modular operation"""
        operation = self.mod_operation.get()
        # You can add field-specific visibility logic here if needed
        # For now, all fields remain visible as they're useful for different operations
        pass

    # Mathematical operation methods
    def perform_quadratic(self):
        """Perform quadratic residue operations"""
        try:
            operation = self.quad_operation.get()
            p_str = self.get_text_content(self.quad_prime)
            
            if not self.validate_input(p_str, "Prime modulus"):
                return
            
            try:
                p = int(p_str)
                if not isprime(p):
                    self.show_warning(f"{p} may not be prime. Results may not be accurate.")
            except ValueError:
                self.show_error("Prime modulus must be an integer")
                return
            
            if operation == "Find Quadratic Residues":
                residues_str = self.get_text_content(self.quad_residues)
                if not self.validate_input(residues_str, "Quadratic residues"):
                    return
                
                try:
                    residues = list(map(int, residues_str.split()))
                except ValueError:
                    self.show_error("Residues must be integers separated by spaces")
                    return
                
                ans = [x for x in range(p) if pow(x, 2, p) in residues]
                
                if ans:
                    output = f"Values x where x² ≡ residue (mod {p}):\n{ans}\n\n"
                    output += f"Statistics:\n"
                    output += f"Minimum value: {min(ans)}\n"
                    output += f"Maximum value: {max(ans)}\n"
                    output += f"Count: {len(ans)}\n"
                    output += f"Percentage of residues: {len(ans)/p*100:.2f}%"
                else:
                    output = "No values found that produce the given quadratic residues."
            
            elif operation == "Legendre Symbol":
                a_str = self.get_text_content(self.quad_number)
                if not self.validate_input(a_str, "Number"):
                    return
                
                try:
                    a = int(a_str)
                except ValueError:
                    self.show_error("Number must be an integer")
                    return
                
                symbol = pow(a, (p - 1) // 2, p)
                if symbol == 1:
                    output = f"Legendre Symbol ({a}/{p}) = 1\n"
                    output += f"Result: {a} is a quadratic residue modulo {p}\n"
                    output += f"This means there exists an x such that x² ≡ {a} (mod {p})"
                elif symbol == p - 1:
                    output = f"Legendre Symbol ({a}/{p}) = -1\n"
                    output += f"Result: {a} is a quadratic non-residue modulo {p}\n"
                    output += f"This means no x exists such that x² ≡ {a} (mod {p})"
                else:
                    output = f"Legendre Symbol ({a}/{p}) = 0\n"
                    output += f"Result: {a} ≡ 0 (mod {p})"
            
            else:  # Check Quadratic Residue
                a_str = self.get_text_content(self.quad_number)
                if not self.validate_input(a_str, "Number"):
                    return
                
                try:
                    a = int(a_str)
                except ValueError:
                    self.show_error("Number must be an integer")
                    return
                
                is_residue = pow(a, (p - 1) // 2, p) == 1
                output = f"Quadratic Residue Test:\n"
                output += f"{a} {'IS' if is_residue else 'IS NOT'} a quadratic residue modulo {p}\n\n"
                
                if is_residue:
                    output += f"This means there exists an x such that x² ≡ {a} (mod {p})"
                    # Try to find the actual square root
                    try:
                        root = self.tonelli_shanks(a, p)
                        output += f"\nSquare roots: ±{root} (mod {p})"
                        output += f"\nVerification: {root}² ≡ {(root*root) % p} (mod {p})"
                    except:
                        pass
                else:
                    output += f"This means no integer x exists such that x² ≡ {a} (mod {p})"
            
            self.update_output(self.quad_output, output)
            self.show_success("Quadratic operation completed successfully")
            
        except Exception as ex:
            self.show_error(f"Quadratic operation failed: {str(ex)}")

    def perform_modular(self):
        """Perform modular operations"""
        try:
            operation = self.mod_operation.get()
            
            if operation == "Modular Square Root":
                n_str = self.get_text_content(self.mod_number)
                p_str = self.get_text_content(self.mod_prime)
                
                if not all([self.validate_input(n_str, "Number"), self.validate_input(p_str, "Prime")]):
                    return
                
                try:
                    n, p = int(n_str), int(p_str)
                    if not isprime(p):
                        self.show_warning(f"{p} may not be prime. Results may not be accurate.")
                except ValueError:
                    self.show_error("All inputs must be integers")
                    return
                
                try:
                    root = self.tonelli_shanks(n, p)
                    other_root = p - root
                    output = f"Modular Square Roots of {n} mod {p}:\n"
                    output += f"√{n} ≡ ±{root} (mod {p})\n"
                    output += f"Solutions: {root} and {other_root}\n\n"
                    output += f"Verification:\n"
                    output += f"{root}² ≡ {(root*root) % p} (mod {p})\n"
                    output += f"{other_root}² ≡ {(other_root*other_root) % p} (mod {p})"
                except Exception as e:
                    output = f"No modular square root exists for {n} mod {p}\n"
                    output += f"Error: {str(e)}\n"
                    # Check if it's a quadratic residue
                    legendre = pow(n, (p - 1) // 2, p)
                    if legendre == p - 1:
                        output += f"Reason: {n} is not a quadratic residue modulo {p}"
            
            elif operation == "Modular Exponentiation":
                base_str = self.get_text_content(self.mod_base)
                exp_str = self.get_text_content(self.mod_exponent)
                mod_str = self.get_text_content(self.mod_prime)
                
                if not all([self.validate_input(base_str, "Base"), 
                           self.validate_input(exp_str, "Exponent"), 
                           self.validate_input(mod_str, "Modulus")]):
                    return
                
                try:
                    base, exp, mod = int(base_str), int(exp_str), int(mod_str)
                    if mod <= 0:
                        self.show_error("Modulus must be positive")
                        return
                except ValueError:
                    self.show_error("All inputs must be integers")
                    return
                
                result = pow(base, exp, mod)
                output = f"Modular Exponentiation:\n"
                output += f"{base}^{exp} ≡ {result} (mod {mod})\n\n"
                output += f"Calculation details:\n"
                output += f"Base: {base}\n"
                output += f"Exponent: {exp}\n"
                output += f"Modulus: {mod}\n"
                output += f"Result: {result}"
            
            elif operation == "Modular Inverse":
                a_str = self.get_text_content(self.mod_number)
                m_str = self.get_text_content(self.mod_prime)
                
                if not all([self.validate_input(a_str, "Number"), self.validate_input(m_str, "Modulus")]):
                    return
                
                try:
                    a, m = int(a_str), int(m_str)
                    if m <= 0:
                        self.show_error("Modulus must be positive")
                        return
                except ValueError:
                    self.show_error("All inputs must be integers")
                    return
                
                try:
                    inv = mod_inverse(a, m)
                    output = f"Modular Inverse:\n"
                    output += f"{a}^(-1) ≡ {inv} (mod {m})\n\n"
                    output += f"Verification:\n"
                    output += f"{a} × {inv} ≡ {(a * inv) % m} (mod {m})\n\n"
                    output += f"Extended Euclidean Algorithm was used to find the inverse."
                except Exception:
                    output = f"No modular inverse exists for {a} mod {m}\n"
                    output += f"Reason: gcd({a}, {m}) ≠ 1\n"
                    output += f"For a modular inverse to exist, {a} and {m} must be coprime."
            
            else:  # Discrete Logarithm
                base_str = self.get_text_content(self.mod_base)
                n_str = self.get_text_content(self.mod_number)
                p_str = self.get_text_content(self.mod_prime)
                
                if not all([self.validate_input(base_str, "Base"), 
                           self.validate_input(n_str, "Number"), 
                           self.validate_input(p_str, "Modulus")]):
                    return
                
                try:
                    base, n, p = int(base_str), int(n_str), int(p_str)
                except ValueError:
                    self.show_error("All inputs must be integers")
                    return
                
                output = f"Discrete Logarithm Computation:\n"
                output += f"Finding x such that {base}^x ≡ {n} (mod {p})\n\n"
                output += f"Note: This computation can be very slow for large values.\n"
                output += f"For cryptographically large numbers, this is computationally infeasible.\n\n"
                
                if p > 10000:
                    output += f"Modulus {p} is too large for practical computation in this interface."
                else:
                    try:
                        result = discrete_log(n, base, p)
                        output += f"Result: x = {result}\n"
                        output += f"Verification: {base}^{result} ≡ {pow(base, result, p)} (mod {p})"
                    except Exception as e:
                        output += f"Could not compute discrete logarithm: {str(e)}"
            
            self.update_output(self.mod_output, output)
            self.show_success("Modular operation completed successfully")
            
        except Exception as ex:
            self.show_error(f"Modular operation failed: {str(ex)}")

    def perform_crt(self):
        """Perform Chinese Remainder Theorem"""
        try:
            remainders_str = self.get_text_content(self.crt_remainders)
            moduli_str = self.get_text_content(self.crt_moduli)
            
            if not all([self.validate_input(remainders_str, "Remainders"), 
                       self.validate_input(moduli_str, "Moduli")]):
                return
            
            try:
                remainders = list(map(int, remainders_str.split()))
                moduli = list(map(int, moduli_str.split()))
            except ValueError:
                self.show_error("All values must be integers separated by spaces")
                return
            
            if len(remainders) != len(moduli):
                self.show_error("Number of remainders must equal number of moduli")
                return
            
            # Check if moduli are pairwise coprime
            for i in range(len(moduli)):
                for j in range(i + 1, len(moduli)):
                    if math.gcd(moduli[i], moduli[j]) != 1:
                        self.show_warning(f"Moduli {moduli[i]} and {moduli[j]} are not coprime. Solution may not be unique.")
            
            # CRT implementation
            total_mod = math.prod(moduli)
            result = 0
            
            output = f"Chinese Remainder Theorem Solution:\n\n"
            output += f"System of congruences:\n"
            for i, (a, m) in enumerate(zip(remainders, moduli)):
                output += f"x ≡ {a} (mod {m})\n"
            
            for a_i, m_i in zip(remainders, moduli):
                p = total_mod // m_i
                inv = mod_inverse(p, m_i)
                contribution = a_i * p * inv
                result += contribution
                
            result = result % total_mod
            
            output += f"\nSolution: x ≡ {result} (mod {total_mod})\n\n"
            output += f"Verification:\n"
            for a, m in zip(remainders, moduli):
                verification = result % m
                status = "✓" if verification == a else "✗"
                output += f"{result} ≡ {verification} (mod {m}) {status}\n"
            
            output += f"\nGeneral solution: x = {result} + k × {total_mod} for any integer k"
            
            self.update_output(self.crt_output, output)
            self.show_success("CRT solved successfully")
            
        except Exception as ex:
            self.show_error(f"CRT computation failed: {str(ex)}")

    def perform_lattice(self):
        """Perform lattice reduction"""
        try:
            v1_str = self.get_text_content(self.lattice_v1)
            v2_str = self.get_text_content(self.lattice_v2)
            
            if not all([self.validate_input(v1_str, "Vector 1"), self.validate_input(v2_str, "Vector 2")]):
                return
            
            try:
                v1 = np.array(list(map(float, v1_str.split())))
                v2 = np.array(list(map(float, v2_str.split())))
            except ValueError:
                self.show_error("Vector components must be numbers separated by spaces")
                return
            
            if len(v1) != len(v2):
                self.show_error("Both vectors must have the same dimension")
                return
            
            if len(v1) < 2:
                self.show_error("Vectors must have at least 2 dimensions")
                return
            
            # Store original vectors for comparison
            orig_v1, orig_v2 = v1.copy(), v2.copy()
            
            # Gaussian reduction
            reduced_v1, reduced_v2 = self.gaussian_reduction(v1, v2)
            
            output = f"Lattice Reduction Results:\n\n"
            output += f"Original vectors:\n"
            output += f"v₁ = {orig_v1}\n"
            output += f"v₂ = {orig_v2}\n\n"
            output += f"Original properties:\n"
            output += f"||v₁|| = {np.linalg.norm(orig_v1):.6f}\n"
            output += f"||v₂|| = {np.linalg.norm(orig_v2):.6f}\n"
            output += f"v₁ · v₂ = {np.dot(orig_v1, orig_v2):.6f}\n\n"
            
            output += f"Reduced vectors:\n"
            output += f"v₁' = {reduced_v1}\n"
            output += f"v₂' = {reduced_v2}\n\n"
            output += f"Reduced properties:\n"
            output += f"||v₁'|| = {np.linalg.norm(reduced_v1):.6f}\n"
            output += f"||v₂'|| = {np.linalg.norm(reduced_v2):.6f}\n"
            output += f"v₁' · v₂' = {np.dot(reduced_v1, reduced_v2):.6f}\n\n"
            
            # Calculate orthogonality measure
            cos_angle = np.dot(reduced_v1, reduced_v2) / (np.linalg.norm(reduced_v1) * np.linalg.norm(reduced_v2))
            angle_deg = np.arccos(np.clip(cos_angle, -1, 1)) * 180 / np.pi
            output += f"Angle between reduced vectors: {angle_deg:.2f}°\n"
            
            if angle_deg > 85 and angle_deg < 95:
                output += "The vectors are nearly orthogonal!"
            
            self.update_output(self.lattice_output, output)
            self.show_success("Lattice reduction completed successfully")
            
        except Exception as ex:
            self.show_error(f"Lattice reduction failed: {str(ex)}")

    def perform_transform(self):
        """Perform number theory transformations"""
        try:
            operation = self.trans_operation.get()
            input_str = self.get_text_content(self.trans_input).strip()
            
            if not self.validate_input(input_str, "Input"):
                return
            
            output = ""
            
            if operation == "Binary to Decimal":
                try:
                    # Remove any spaces or prefixes
                    clean_input = input_str.replace(" ", "").replace("0b", "")
                    result = int(clean_input, 2)
                    output = f"Binary to Decimal Conversion:\n"
                    output += f"Binary: {clean_input}\n"
                    output += f"Decimal: {result}\n\n"
                    output += f"Calculation: "
                    # Show the calculation for educational purposes
                    binary_digits = clean_input[::-1]  # Reverse for easier indexing
                    calc_parts = []
                    for i, digit in enumerate(binary_digits):
                        if digit == '1':
                            calc_parts.append(f"2^{i}")
                    output += " + ".join(calc_parts) + f" = {result}"
                except ValueError:
                    self.show_error("Invalid binary number. Use only 0s and 1s.")
                    return
            
            elif operation == "Decimal to Binary":
                try:
                    decimal = int(input_str)
                    if decimal < 0:
                        self.show_error("Please enter a non-negative integer")
                        return
                    result = bin(decimal)[2:]
                    output = f"Decimal to Binary Conversion:\n"
                    output += f"Decimal: {decimal}\n"
                    output += f"Binary: {result}\n\n"
                    
                    # Show division method for educational purposes
                    if decimal > 0 and decimal < 1000:  # Limit for readability
                        output += f"Division method:\n"
                        temp = decimal
                        steps = []
                        while temp > 0:
                            remainder = temp % 2
                            quotient = temp // 2
                            steps.append(f"{temp} ÷ 2 = {quotient} remainder {remainder}")
                            temp = quotient
                        output += "\n".join(steps)
                        output += f"\nReading remainders from bottom to top: {result}"
                except ValueError:
                    self.show_error("Invalid decimal number")
                    return
            
            elif operation == "Decimal to Hex":
                try:
                    decimal = int(input_str)
                    if decimal < 0:
                        self.show_error("Please enter a non-negative integer")
                        return
                    result = hex(decimal)[2:].upper()
                    output = f"Decimal to Hexadecimal Conversion:\n"
                    output += f"Decimal: {decimal}\n"
                    output += f"Hexadecimal: {result}\n"
                    output += f"Hexadecimal (with prefix): 0x{result}"
                except ValueError:
                    self.show_error("Invalid decimal number")
                    return
            
            elif operation == "Hex to Decimal":
                try:
                    # Remove common prefixes and clean input
                    clean_input = input_str.replace("0x", "").replace("0X", "").replace(" ", "")
                    result = int(clean_input, 16)
                    output = f"Hexadecimal to Decimal Conversion:\n"
                    output += f"Hexadecimal: {clean_input.upper()}\n"
                    output += f"Decimal: {result}\n\n"
                    
                    # Show calculation for educational purposes
                    if len(clean_input) <= 4:  # Limit for readability
                        output += f"Calculation: "
                        hex_digits = clean_input[::-1].upper()  # Reverse for easier indexing
                        calc_parts = []
                        for i, digit in enumerate(hex_digits):
                            if digit != '0':
                                digit_value = int(digit, 16)
                                calc_parts.append(f"{digit_value}×16^{i}")
                        if calc_parts:
                            output += " + ".join(calc_parts) + f" = {result}"
                except ValueError:
                    self.show_error("Invalid hexadecimal number. Use digits 0-9 and letters A-F.")
                    return
            
            elif operation == "Prime Factorization":
                try:
                    number = int(input_str)
                    if number <= 0:
                        self.show_error("Please enter a positive integer")
                        return
                    elif number == 1:
                        output = f"Prime Factorization of 1:\n1 has no prime factors (by definition)"
                    else:
                        factors = factorint(number)
                        factor_str = " × ".join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items()])
                        
                        output = f"Prime Factorization of {number}:\n"
                        output += f"{number} = {factor_str}\n\n"
                        output += f"Prime factors: {list(factors.keys())}\n"
                        output += f"Factor details:\n"
                        for prime, exponent in factors.items():
                            output += f"  {prime}^{exponent} = {prime**exponent}\n"
                        
                        # Additional info
                        total_factors = sum(factors.values())
                        unique_primes = len(factors)
                        output += f"\nTotal prime factors (with multiplicity): {total_factors}\n"
                        output += f"Distinct prime factors: {unique_primes}\n"
                        
                        if unique_primes == 1:
                            output += f"{number} is a prime power!"
                        elif unique_primes == total_factors:
                            output += f"{number} is square-free!"
                            
                except ValueError:
                    self.show_error("Invalid number for factorization")
                    return
            
            elif operation == "Primality Test":
                try:
                    number = int(input_str)
                    if number <= 1:
                        output = f"Primality Test for {number}:\n"
                        output += f"{number} is neither prime nor composite (by definition)"
                    else:
                        is_prime = isprime(number)
                        output = f"Primality Test for {number}:\n"
                        output += f"{number} is {'PRIME' if is_prime else 'COMPOSITE'}\n\n"
                        
                        if not is_prime and number > 1:
                            # Show factors for composite numbers
                            factors = factorint(number)
                            smallest_factor = min(factors.keys())
                            largest_factor = max(factors.keys())
                            
                            output += f"Factorization evidence:\n"
                            if smallest_factor != number:
                                output += f"Smallest prime factor: {smallest_factor}\n"
                                output += f"Largest prime factor: {largest_factor}\n"
                                output += f"{number} = {smallest_factor} × {number // smallest_factor}\n"
                        
                        elif is_prime:
                            output += f"Properties of prime {number}:\n"
                            if number == 2:
                                output += "- Only even prime number\n"
                            elif number % 4 == 1:
                                output += f"- Prime of form 4k+1 (k = {(number-1)//4})\n"
                            elif number % 4 == 3:
                                output += f"- Prime of form 4k+3 (k = {(number-3)//4})\n"
                            
                            # Check if it's a special prime
                            if number > 2:
                                prev_prime_check = isprime(number - 2)
                                next_prime_check = isprime(number + 2)
                                if prev_prime_check:
                                    output += f"- Twin prime with {number - 2}\n"
                                if next_prime_check:
                                    output += f"- Twin prime with {number + 2}\n"
                                    
                except ValueError:
                    self.show_error("Invalid number for primality test")
                    return
            
            self.update_output(self.trans_output, output)
            self.show_success("Transformation completed successfully")
            
        except Exception as ex:
            self.show_error(f"Transformation failed: {str(ex)}")

    # Helper methods
    def tonelli_shanks(self, n, p):
        """Tonelli-Shanks algorithm for modular square root"""
        def legendre(a, p):
            return pow(a, (p - 1) // 2, p)
        
        if legendre(n, p) != 1:
            raise ValueError("Not a quadratic residue")
        
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
                    raise ValueError("Algorithm failed")
            
            b = pow(c, 1 << (m - i - 1), p)
            r = (r * b) % p
            t = (t * b * b) % p
            c = (b * b) % p
            m = i
        
        return r

    def gaussian_reduction(self, v1, v2):
        """Gaussian reduction of two vectors"""
        v1, v2 = v1.copy(), v2.copy()
        
        while True:
            if np.dot(v2, v2) < np.dot(v1, v1):
                v1, v2 = v2, v1
            
            if np.dot(v1, v1) == 0:
                break
                
            m = round(np.dot(v1, v2) / np.dot(v1, v1))
            if m == 0:
                break
            
            v2 = v2 - m * v1
        
        return v1, v2

    # Clear methods
    def clear_quadratic(self):
        """Clear quadratic tab inputs"""
        for widget in [self.quad_prime, self.quad_number, self.quad_residues]:
            if hasattr(widget, 'delete'):
                widget.delete(0, tk.END)
        self.update_output(self.quad_output, "")

    def clear_modular(self):
        """Clear modular tab inputs"""
        for widget in [self.mod_number, self.mod_exponent, self.mod_prime, self.mod_base]:
            if hasattr(widget, 'delete'):
                widget.delete(0, tk.END)
        self.update_output(self.mod_output, "")

    def clear_crt(self):
        """Clear CRT tab inputs"""
        for widget in [self.crt_remainders, self.crt_moduli]:
            if hasattr(widget, 'delete'):
                widget.delete(0, tk.END)
        self.update_output(self.crt_output, "")

    def clear_lattice(self):
        """Clear lattice tab inputs"""
        for widget in [self.lattice_v1, self.lattice_v2]:
            if hasattr(widget, 'delete'):
                widget.delete(0, tk.END)
        self.update_output(self.lattice_output, "")

    def clear_transform(self):
        """Clear transforms tab inputs"""
        if hasattr(self.trans_input, 'delete'):
            self.trans_input.delete(0, tk.END)
        self.update_output(self.trans_output, "")

    def _return_to_main(self):
        """Return to the main welcome screen"""
        if self.main_window:
            self.main_window.show_welcome()
        else:
            # Fallback method if main_window reference is not available
            try:
                # Clear the current content and show welcome
                for widget in self.parent.winfo_children():
                    widget.destroy()
                # Try to find the main window through the widget hierarchy
                root = self.parent.winfo_toplevel()
                if hasattr(root, 'main_window'):
                    root.main_window.show_welcome()
            except Exception:
                # Last resort fallback
                for widget in self.parent.winfo_children():
                    widget.destroy()