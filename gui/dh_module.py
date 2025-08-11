import tkinter as tk
from tkinter import ttk
import random
from gui.base_module import BaseGUIModule
from DiffieHellman.dh import decrypt_flag, decrypt_direct, calculate_shared_secret


class DHModule(BaseGUIModule):
    def __init__(self, parent, main_window=None):
        super().__init__(parent, "Diffie-Hellman")
        self.main_window = main_window

    def init_module(self):
        # Create multiple tabs like RSA module
        self.calculation_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.calculation_frame, text="Calculations")
        self.create_calculation_tab()

        self.decryption_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.decryption_frame, text="Decryption")
        self.create_decryption_tab()

        self.utilities_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.utilities_frame, text="Utilities")
        self.create_utilities_tab()

    def create_calculation_tab(self):
        """Tab for basic DH calculations"""
        input_frame = self.create_input_frame(self.calculation_frame, "Diffie-Hellman Calculations")
        
        # Operation selection - matching Base encoding style
        operation_frame = ttk.Frame(input_frame, style='Main.TFrame')
        operation_frame.pack(fill='x')
        ttk.Label(operation_frame, text="Operation:", style='Info.TLabel').pack(anchor='w')
        self.calc_operation = ttk.Combobox(operation_frame, values=[
            "Modular Exponentiation (g^a mod p)",
            "Calculate Shared Secret (A^b mod p)",
            "Find Generator"
        ], state='readonly')
        self.calc_operation.set("Calculate Shared Secret (A^b mod p)")
        self.calc_operation.pack(fill='x', pady=(0, 10))
        self.calc_operation.bind('<<ComboboxSelected>>', self.on_calc_operation_change)

        # Parameters frame with left/right layout like RSA
        params_frame = ttk.Frame(input_frame, style='Main.TFrame')
        params_frame.pack(fill='x', pady=(0, 10))

        left_frame = ttk.Frame(params_frame, style='Main.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.calc_base = self.create_text_input(left_frame, "Base/Public value (g/A):")
        self.calc_exponent = self.create_text_input(left_frame, "Exponent/Private key (a/b):")

        right_frame = ttk.Frame(params_frame, style='Main.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        self.calc_modulus = self.create_text_input(right_frame, "Prime modulus (p):")

        # Container for any dynamic content (ensures proper positioning)
        self.calc_dynamic_container = ttk.Frame(input_frame, style='Main.TFrame')
        self.calc_dynamic_container.pack(fill='x', pady=(0, 10))

        # Buttons (placed after all content)
        button_frame = self.create_button_frame(input_frame)
        self.create_action_button(button_frame, "Calculate", self.perform_calculation, 0)
        self.create_action_button(button_frame, "Clear", self.clear_calculation, 1)
        self.create_return_button(button_frame, self._return_to_main)

        # Output
        output_frame = self.create_output_frame(self.calculation_frame, "Calculation Result")
        self.calc_output = self.create_output_text(output_frame)

    def create_decryption_tab(self):
        """Tab for DH-based decryption operations"""
        input_frame = self.create_input_frame(self.decryption_frame, "Diffie-Hellman Decryption")
        
        # Decryption mode selection - matching Base encoding style
        mode_frame = ttk.Frame(input_frame, style='Main.TFrame')
        mode_frame.pack(fill='x')
        ttk.Label(mode_frame, text="Decryption Mode:", style='Info.TLabel').pack(anchor='w')
        self.dec_mode = ttk.Combobox(mode_frame, values=[
            "Decrypt using Shared Secret",
            "Decrypt using Direct Parameters"
        ], state='readonly')
        self.dec_mode.set("Decrypt using Shared Secret")
        self.dec_mode.pack(fill='x', pady=(0, 10))
        self.dec_mode.bind('<<ComboboxSelected>>', self.on_dec_mode_change)

        # Shared secret mode frame
        self.shared_secret_frame = ttk.Frame(input_frame, style='Main.TFrame')
        self.shared_secret_frame.pack(fill='x', pady=(0, 10))
        self.dec_shared_secret = self.create_text_input(self.shared_secret_frame, "Shared Secret:")

        # DH parameters mode frame  
        self.dh_params_frame = ttk.Frame(input_frame, style='Main.TFrame')
        
        params_frame = ttk.Frame(self.dh_params_frame, style='Main.TFrame')
        params_frame.pack(fill='x', pady=(0, 10))

        left_frame = ttk.Frame(params_frame, style='Main.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.dec_public_value = self.create_text_input(left_frame, "Public value (A):")
        self.dec_private_key = self.create_text_input(left_frame, "Private key (b):")

        right_frame = ttk.Frame(params_frame, style='Main.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        self.dec_prime_modulus = self.create_text_input(right_frame, "Prime modulus (p):")

        # Common decryption parameters
        common_frame = ttk.Frame(input_frame, style='Main.TFrame')
        common_frame.pack(fill='x', pady=(0, 10))
        
        crypto_params_frame = ttk.Frame(common_frame, style='Main.TFrame')
        crypto_params_frame.pack(fill='x', pady=(0, 10))

        left_crypto = ttk.Frame(crypto_params_frame, style='Main.TFrame')
        left_crypto.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.dec_iv = self.create_text_input(left_crypto, "IV (hex):")
        
        right_crypto = ttk.Frame(crypto_params_frame, style='Main.TFrame')
        right_crypto.pack(side='right', fill='both', expand=True, padx=(5, 0))

        self.dec_ciphertext = self.create_text_input(common_frame, "Ciphertext (hex):", multiline=True)

        # Buttons
        button_frame = self.create_button_frame(input_frame)
        self.create_action_button(button_frame, "Decrypt", self.perform_decryption, 0)
        self.create_action_button(button_frame, "Clear", self.clear_decryption, 1)
        self.create_return_button(button_frame, self._return_to_main)

        # Output
        output_frame = self.create_output_frame(self.decryption_frame, "Decryption Result")
        self.dec_output = self.create_output_text(output_frame)

        # Set initial visibility
        self.on_dec_mode_change()

    def create_utilities_tab(self):
        """Tab for DH utilities like generator finding"""
        input_frame = self.create_input_frame(self.utilities_frame, "Diffie-Hellman Utilities")
        
        # Utility operation selection - matching Base encoding style
        operation_frame = ttk.Frame(input_frame, style='Main.TFrame')
        operation_frame.pack(fill='x')
        ttk.Label(operation_frame, text="Utility Operation:", style='Info.TLabel').pack(anchor='w')
        self.util_operation = ttk.Combobox(operation_frame, values=[
            "Find Generator",
            "Verify Generator",
            "Generate Key Pair"
        ], state='readonly')
        self.util_operation.set("Find Generator")
        self.util_operation.pack(fill='x', pady=(0, 10))
        self.util_operation.bind('<<ComboboxSelected>>', self.on_util_operation_change)

        # Parameters
        self.util_prime = self.create_text_input(input_frame, "Prime modulus (p):")
        
        # Container for dynamic content (ensures proper positioning)
        self.util_dynamic_container = ttk.Frame(input_frame, style='Main.TFrame')
        self.util_dynamic_container.pack(fill='x', pady=(0, 10))
        
        # Optional parameters frame (will be added to dynamic container)
        self.util_optional_frame = ttk.Frame(self.util_dynamic_container, style='Main.TFrame')
        self.util_generator = self.create_text_input(self.util_optional_frame, "Generator to verify (g):")

        # Buttons (placed after dynamic container)
        button_frame = self.create_button_frame(input_frame)
        self.create_action_button(button_frame, "Execute", self.perform_utility, 0)
        self.create_action_button(button_frame, "Clear", self.clear_utilities, 1)
        self.create_return_button(button_frame, self._return_to_main)

        # Output
        output_frame = self.create_output_frame(self.utilities_frame, "Utility Result")
        self.util_output = self.create_output_text(output_frame)

        # Set initial visibility
        self.on_util_operation_change()

    def on_calc_operation_change(self, event=None):
        """Update labels based on calculation operation"""
        operation = self.calc_operation.get()
        if operation == "Find Generator":
            # Hide exponent field for generator finding
            pass  # Could implement specific UI changes if needed

    def on_dec_mode_change(self, event=None):
        """Toggle between shared secret and DH parameters modes"""
        mode = self.dec_mode.get()
        if mode == "Decrypt using Shared Secret":
            self.dh_params_frame.pack_forget()
            self.shared_secret_frame.pack(fill='x', pady=(0, 10))
        else:  # "Decrypt using Direct Parameters"
            self.shared_secret_frame.pack_forget()
            self.dh_params_frame.pack(fill='x', pady=(0, 10))

    def on_util_operation_change(self, event=None):
        """Show/hide optional parameters based on utility operation"""
        operation = self.util_operation.get()
        if operation == "Verify Generator":
            self.util_optional_frame.pack(fill='x', pady=(0, 10))
        else:
            self.util_optional_frame.pack_forget()

    def perform_calculation(self):
        """Perform the selected calculation"""
        try:
            operation = self.calc_operation.get()
            
            if operation == "Find Generator":
                p_str = self.get_text_content(self.calc_modulus)
                if not self.validate_input(p_str, "Prime modulus (p)"):
                    return
                
                try:
                    p = int(p_str)
                    if p <= 2:
                        self.show_error("Prime modulus must be greater than 2")
                        return
                except ValueError:
                    self.show_error("Prime modulus must be an integer")
                    return
                
                self.update_output(self.calc_output, "Searching for generator... This may take a moment.")
                self.parent.update()  # Update GUI to show the message
                
                generator = self.find_generator(p)
                if generator:
                    self.update_output(self.calc_output, f"First generator found: {generator}")
                    self.show_success("Generator found successfully")
                else:
                    self.update_output(self.calc_output, "No generator found within search limit")
                    self.show_warning("No generator found (search was limited to prevent long delays)")
            
            else:  # Modular exponentiation or shared secret calculation
                base_str = self.get_text_content(self.calc_base)
                exp_str = self.get_text_content(self.calc_exponent)
                mod_str = self.get_text_content(self.calc_modulus)
                
                if not all([
                    self.validate_input(base_str, "Base/Public value"),
                    self.validate_input(exp_str, "Exponent/Private key"),
                    self.validate_input(mod_str, "Prime modulus")
                ]):
                    return
                
                try:
                    base = int(base_str)
                    exponent = int(exp_str)
                    modulus = int(mod_str)
                    
                    if modulus <= 0:
                        self.show_error("Modulus must be positive")
                        return
                    if base < 0:
                        self.show_error("Base cannot be negative")
                        return
                    if exponent < 0:
                        self.show_error("Exponent cannot be negative")
                        return
                        
                except ValueError:
                    self.show_error("All parameters must be integers")
                    return
                
                result = calculate_shared_secret(base, exponent, modulus)
                
                if operation == "Modular Exponentiation (g^a mod p)":
                    output = f"Result: {base}^{exponent} mod {modulus} = {result}\nHex: 0x{result:x}"
                else:  # Shared secret
                    output = f"Shared Secret: {result}\nHex: 0x{result:x}"
                
                self.update_output(self.calc_output, output)
                self.show_success("Calculation completed successfully")
                
        except Exception as ex:
            self.show_error(f"Calculation failed: {str(ex)}")

    def perform_decryption(self):
        """Perform the selected decryption"""
        try:
            mode = self.dec_mode.get()
            iv_str = self.get_text_content(self.dec_iv)
            ct_str = self.get_text_content(self.dec_ciphertext)
            
            # Validate hex input
            if not self.validate_hex_input(iv_str, "IV"):
                return
            if not self.validate_hex_input(ct_str, "Ciphertext"):
                return
            
            if mode == "Decrypt using Shared Secret":
                shared_str = self.get_text_content(self.dec_shared_secret)
                if not self.validate_input(shared_str, "Shared Secret"):
                    return
                
                try:
                    shared_secret = int(shared_str)
                    if shared_secret <= 0:
                        self.show_error("Shared secret must be positive")
                        return
                except ValueError:
                    self.show_error("Shared secret must be an integer")
                    return
                
                result = decrypt_flag(shared_secret, iv_str, ct_str)
                output = f"Shared Secret Used: {shared_secret}\nDecrypted message: {result}"
                
            else:  # "Decrypt using Direct Parameters"
                A_str = self.get_text_content(self.dec_public_value)
                b_str = self.get_text_content(self.dec_private_key)
                p_str = self.get_text_content(self.dec_prime_modulus)
                
                if not all([
                    self.validate_input(A_str, "Public value (A)"),
                    self.validate_input(b_str, "Private key (b)"),
                    self.validate_input(p_str, "Prime modulus (p)")
                ]):
                    return
                
                try:
                    A = int(A_str)
                    b = int(b_str)
                    p = int(p_str)
                    
                    if p <= 0 or A <= 0 or b <= 0:
                        self.show_error("A, b, and p must be positive integers")
                        return
                        
                except ValueError:
                    self.show_error("A, b, and p must be integers")
                    return
                
                result_bytes = decrypt_direct(A, b, p, iv_str, ct_str)
                
                try:
                    # Try UTF-8 first, then ASCII, then display as bytes
                    try:
                        result_text = result_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        result_text = result_bytes.decode('ascii', errors='ignore')
                except Exception:
                    result_text = f"Raw bytes: {result_bytes}"
                
                # Calculate shared secret for reference
                shared_secret = calculate_shared_secret(A, b, p)
                output = f"Calculated Shared Secret: {shared_secret} (0x{shared_secret:x})\nDecrypted message: {result_text}"
            
            self.update_output(self.dec_output, output)
            self.show_success("Decryption completed successfully")
            
        except Exception as ex:
            self.show_error(f"Decryption failed: {str(ex)}")

    def perform_utility(self):
        """Perform the selected utility operation"""
        try:
            operation = self.util_operation.get()
            p_str = self.get_text_content(self.util_prime)
            
            if not self.validate_input(p_str, "Prime modulus (p)"):
                return
            
            try:
                p = int(p_str)
                if p <= 2:
                    self.show_error("Prime modulus must be greater than 2")
                    return
            except ValueError:
                self.show_error("Prime modulus must be an integer")
                return
            
            if operation == "Find Generator":
                self.update_output(self.util_output, "Searching for generator... This may take a moment.")
                self.parent.update()  # Update GUI to show the message
                
                generator = self.find_generator(p)
                if generator:
                    output = f"First generator found: {generator}"
                    self.show_success("Generator found successfully")
                else:
                    output = "No generator found within search limit"
                    self.show_warning("No generator found (search was limited)")
            
            elif operation == "Verify Generator":
                g_str = self.get_text_content(self.util_generator)
                if not self.validate_input(g_str, "Generator to verify"):
                    return
                
                try:
                    g = int(g_str)
                    if g <= 1:
                        self.show_error("Generator must be greater than 1")
                        return
                except ValueError:
                    self.show_error("Generator must be an integer")
                    return
                
                is_gen = self.verify_generator(g, p)
                if is_gen:
                    output = f"{g} is a valid generator for prime {p}"
                    self.show_success("Generator verification passed")
                else:
                    output = f"{g} is NOT a generator for prime {p}"
                    self.show_warning("Generator verification failed")
            
            else:  # "Generate Key Pair"
                self.update_output(self.util_output, "Finding generator and generating key pair...")
                self.parent.update()  # Update GUI to show the message
                
                generator = self.find_generator(p)
                if not generator:
                    output = "Cannot generate key pair: no generator found for the given prime"
                    self.show_error("No generator available")
                else:
                    private_key = random.randint(2, p-2)
                    public_key = pow(generator, private_key, p)
                    output = (f"Generated key pair:\n"
                             f"Prime (p): {p}\n"
                             f"Generator (g): {generator}\n"
                             f"Private key (a): {private_key}\n"
                             f"Public key (A): {public_key} (0x{public_key:x})")
                    self.show_success("Key pair generated successfully")
            
            self.update_output(self.util_output, output)
            
        except Exception as ex:
            self.show_error(f"Utility operation failed: {str(ex)}")

    def find_generator(self, p):
        """
        Find a generator for the given prime using the same algorithm as your backend code.
        Uses a reasonable search limit to avoid GUI freezing.
        """
        # Limit search to prevent GUI freezing on large primes
        search_limit = min(p, 1000)
        
        for k in range(2, search_limit):
            is_generator = True
            # Use the same logic as your backend code but with reasonable limits
            check_limit = min(p, 100)  # Limit the inner loop as well
            
            for n in range(2, check_limit):
                if pow(k, n, p) == k:
                    is_generator = False
                    break
            
            if is_generator:
                return k
                
        return None

    def verify_generator(self, g, p):
        """
        Verify if g is a generator for prime p using your algorithm.
        """
        if g <= 1 or g >= p:
            return False
        
        # Use the same verification logic as your backend code
        check_limit = min(p, 100)  # Reasonable limit for GUI responsiveness
        
        for n in range(2, check_limit):
            if pow(g, n, p) == g:
                return False
        return True

    def validate_hex_input(self, hex_str, field_name):
        """Validate that input is valid hexadecimal"""
        if not hex_str.strip():
            self.show_error(f"{field_name} cannot be empty")
            return False
        
        # Remove common hex prefixes if present
        clean_hex = hex_str.strip().lower()
        if clean_hex.startswith('0x'):
            clean_hex = clean_hex[2:]
        
        try:
            bytes.fromhex(clean_hex)
            return True
        except ValueError:
            self.show_error(f"{field_name} must be valid hexadecimal")
            return False

    # Clear methods for each tab
    def clear_calculation(self):
        """Clear calculation tab inputs"""
        for widget in [self.calc_base, self.calc_exponent, self.calc_modulus]:
            if hasattr(widget, 'delete'):
                widget.delete(0, tk.END)
        self.update_output(self.calc_output, "")

    def clear_decryption(self):
        """Clear decryption tab inputs"""
        widgets_to_clear = [
            self.dec_shared_secret, self.dec_public_value, self.dec_private_key,
            self.dec_prime_modulus, self.dec_iv
        ]
        
        for widget in widgets_to_clear:
            try:
                if hasattr(widget, 'delete'):
                    widget.delete(0, tk.END)
            except Exception:
                pass
        
        try:
            if hasattr(self.dec_ciphertext, 'delete'):
                if hasattr(self.dec_ciphertext, 'index'):  # Text widget
                    self.dec_ciphertext.delete("1.0", tk.END)
                else:  # Entry widget
                    self.dec_ciphertext.delete(0, tk.END)
        except Exception:
            pass
        
        self.update_output(self.dec_output, "")

    def clear_utilities(self):
        """Clear utilities tab inputs"""
        for widget in [self.util_prime, self.util_generator]:
            if hasattr(widget, 'delete'):
                widget.delete(0, tk.END)
        self.update_output(self.util_output, "")

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