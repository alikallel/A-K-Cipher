"""
RSA GUI Module
"""
import tkinter as tk
from tkinter import ttk
from gui.base_module import BaseGUIModule
from RSA.encrypt import rsa_encrypt_normal, rsa_encrypt_single_prime
from RSA.decrypt import RSACracker
from RSA.factorize import factorize


class RSAModule(BaseGUIModule):
    def __init__(self, parent, main_window=None):
        super().__init__(parent, "RSA")
        self.main_window = main_window

    def init_module(self):
        self.encryption_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.encryption_frame, text="Encryption")
        self.create_encryption_tab()

        self.decryption_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.decryption_frame, text="Decryption")
        self.create_decryption_tab()

        self.factorization_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.factorization_frame, text="Factorization")
        self.create_factorization_tab()

    def create_encryption_tab(self):
        input_frame = self.create_input_frame(self.encryption_frame, "RSA Encryption")
        self.enc_message = self.create_text_input(input_frame, "Message to encrypt:", multiline=True)

        params_frame = ttk.Frame(input_frame, style='Main.TFrame')
        params_frame.pack(fill='x', pady=(0, 10))

        left_frame = ttk.Frame(params_frame, style='Main.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.enc_n = self.create_text_input(left_frame, "Modulus (n):")
        self.enc_e = self.create_text_input(left_frame, "Public Exponent (e):")

        right_frame = ttk.Frame(params_frame, style='Main.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        self.enc_p = self.create_text_input(right_frame, "Prime p (optional):")
        self.enc_flag_format = self.create_text_input(right_frame, "Flag Format (optional):")

        button_frame = self.create_button_frame(input_frame)
        self.create_action_button(button_frame, "Encrypt", self.encrypt_message, 0)
        self.create_action_button(button_frame, "Clear", self.clear_encryption, 1)
        self.create_return_button(button_frame, self._return_to_main)

        output_frame = self.create_output_frame(self.encryption_frame, "Encryption Result")
        self.enc_output = self.create_output_text(output_frame)

    def create_decryption_tab(self):
        input_frame = self.create_input_frame(self.decryption_frame, "RSA Decryption")
        self.dec_mode = self.create_combobox(
            input_frame,
            "Decryption Mode:",
            ["Single Ciphertext", "Common Modulus Attack"],
            "Single Ciphertext",
        )
        self.dec_mode.bind('<<ComboboxSelected>>', self.on_mode_change)

        self.single_frame = ttk.Frame(input_frame, style='Main.TFrame')
        self.single_frame.pack(fill='x', pady=(0, 10))
        self.dec_ciphertext = self.create_text_input(self.single_frame, "Ciphertext:")

        params_frame = ttk.Frame(self.single_frame, style='Main.TFrame')
        params_frame.pack(fill='x', pady=(0, 10))

        left_frame = ttk.Frame(params_frame, style='Main.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.dec_n = self.create_text_input(left_frame, "Modulus (n):")
        self.dec_e = self.create_text_input(left_frame, "Public Exponent (e):")

        right_frame = ttk.Frame(params_frame, style='Main.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        self.dec_p = self.create_text_input(right_frame, "Prime p (optional):")
        self.dec_q = self.create_text_input(right_frame, "Prime q (optional):")

        self.common_frame = ttk.Frame(input_frame, style='Main.TFrame')
        self.dec_c1 = self.create_text_input(self.common_frame, "Ciphertext 1 (c1):")
        self.dec_c2 = self.create_text_input(self.common_frame, "Ciphertext 2 (c2):")

        common_params_frame = ttk.Frame(self.common_frame, style='Main.TFrame')
        common_params_frame.pack(fill='x', pady=(0, 10))
        left_common = ttk.Frame(common_params_frame, style='Main.TFrame')
        left_common.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.dec_e1 = self.create_text_input(left_common, "Public Exponent 1 (e1):")
        self.dec_n_common = self.create_text_input(left_common, "Modulus (n):")
        right_common = ttk.Frame(common_params_frame, style='Main.TFrame')
        right_common.pack(side='right', fill='both', expand=True, padx=(5, 0))
        self.dec_e2 = self.create_text_input(right_common, "Public Exponent 2 (e2):")

        button_frame = self.create_button_frame(input_frame)
        self.create_action_button(button_frame, "Decrypt", self.decrypt_message, 0)
        self.create_action_button(button_frame, "Clear", self.clear_decryption, 1)
        self.create_return_button(button_frame, self._return_to_main)

        output_frame = self.create_output_frame(self.decryption_frame, "Decryption Result")
        self.dec_output = self.create_output_text(output_frame)

    def create_factorization_tab(self):
        input_frame = self.create_input_frame(self.factorization_frame, "RSA Factorization")
        self.factor_n = self.create_text_input(input_frame, "RSA Modulus (n) to factorize:")
        button_frame = self.create_button_frame(input_frame)
        self.create_action_button(button_frame, "Factorize", self.factorize_number, 0)
        self.create_action_button(button_frame, "Clear", self.clear_factorization, 1)
        self.create_return_button(button_frame, self._return_to_main)
        output_frame = self.create_output_frame(self.factorization_frame, "Factorization Result")
        self.factor_output = self.create_output_text(output_frame)

    def on_mode_change(self, event=None):
        mode = self.dec_mode.get()
        if mode == "Single Ciphertext":
            self.common_frame.pack_forget()
            self.single_frame.pack(fill='x', pady=(0, 10))
        else:
            self.single_frame.pack_forget()
            self.common_frame.pack(fill='x', pady=(0, 10))

    def encrypt_message(self):
        try:
            message = self.get_text_content(self.enc_message)
            n_str = self.get_text_content(self.enc_n)
            e_str = self.get_text_content(self.enc_e)
            p_str = self.get_text_content(self.enc_p)
            flag_format = self.get_text_content(self.enc_flag_format)

            if not self.validate_input(message, "Message"):
                return
            if not self.validate_input(n_str, "Modulus (n)"):
                return
            if not self.validate_input(e_str, "Public Exponent (e)"):
                return

            try:
                n = int(n_str)
                e = int(e_str)
                p = int(p_str) if p_str else None
            except ValueError:
                self.show_error("n, e, and p must be integers (if provided)")
                return

            if p is not None and p == n:
                ciphertext = rsa_encrypt_single_prime(message, n, e, flag_format or None)
            else:
                ciphertext = rsa_encrypt_normal(message, n, e, flag_format or None)

            output = f"Ciphertext (int): {ciphertext}\nCiphertext (hex): {hex(ciphertext)}"
            self.update_output(self.enc_output, output)
            self.show_success("Encryption completed")
        except Exception as ex:
            self.show_error(f"Encryption failed: {ex}")

    def _parse_int_or_hex(self, value: str) -> int:
        value = value.strip()
        try:
            return int(value)
        except ValueError:
            if value.lower().startswith('0x'):
                return int(value, 16)
            return int(value, 16)

    def decrypt_message(self):
        try:
            mode = self.dec_mode.get()
            cracker = RSACracker(verbose=False)

            if mode == "Single Ciphertext":
                c_str = self.get_text_content(self.dec_ciphertext)
                n_str = self.get_text_content(self.dec_n)
                e_str = self.get_text_content(self.dec_e)
                p_str = self.get_text_content(self.dec_p)
                q_str = self.get_text_content(self.dec_q)

                if not self.validate_input(c_str, "Ciphertext") or not self.validate_input(n_str, "Modulus (n)"):
                    return

                try:
                    c = self._parse_int_or_hex(c_str)
                    n = int(n_str)
                    e = int(e_str) if e_str else 65537
                    p = int(p_str) if p_str else None
                    q = int(q_str) if q_str else None
                except ValueError:
                    self.show_error("Invalid numeric input. Use decimal or hex for ciphertext; integers for n,e,p,q.")
                    return

                plaintext_int = cracker.decrypt_message(c, n, e, p=p, q=q)
                if plaintext_int is None:
                    self.show_warning("Decryption failed. Try providing more parameters or different method.")
                    return

                try:
                    from Crypto.Util.number import long_to_bytes
                    plaintext_bytes = long_to_bytes(plaintext_int)
                    plaintext_utf8 = plaintext_bytes.decode('utf-8', errors='ignore')
                except Exception:
                    plaintext_utf8 = ""

                output = (
                    f"Plaintext (int): {plaintext_int}\n"
                    f"Plaintext (hex): {hex(plaintext_int)}\n"
                    f"Plaintext (utf-8): {plaintext_utf8}"
                )
                self.update_output(self.dec_output, output)
                self.show_success("Decryption completed")

            else:  # Common modulus attack
                c1_str = self.get_text_content(self.dec_c1)
                c2_str = self.get_text_content(self.dec_c2)
                e1_str = self.get_text_content(self.dec_e1)
                e2_str = self.get_text_content(self.dec_e2)
                n_str = self.get_text_content(self.dec_n_common)

                for field, name in [
                    (c1_str, 'Ciphertext 1 (c1)'),
                    (c2_str, 'Ciphertext 2 (c2)'),
                    (e1_str, 'Public Exponent 1 (e1)'),
                    (e2_str, 'Public Exponent 2 (e2)'),
                    (n_str, 'Modulus (n)'),
                ]:
                    if not self.validate_input(field, name):
                        return

                try:
                    c1 = self._parse_int_or_hex(c1_str)
                    c2 = self._parse_int_or_hex(c2_str)
                    e1 = int(e1_str)
                    e2 = int(e2_str)
                    n = int(n_str)
                except ValueError:
                    self.show_error("Invalid inputs. c1,c2 can be int or hex; e1,e2,n must be integers.")
                    return

                result_int = RSACracker(verbose=False).common_modulus_attack(c1, c2, e1, e2, n)
                if result_int is None:
                    self.show_warning("Common modulus attack failed. Ensure gcd(e1, e2) = 1.")
                    return

                try:
                    from Crypto.Util.number import long_to_bytes
                    result_bytes = long_to_bytes(result_int)
                    result_utf8 = result_bytes.decode('utf-8', errors='ignore')
                except Exception:
                    result_utf8 = ""

                output = (
                    f"Recovered (int): {result_int}\n"
                    f"Recovered (hex): {hex(result_int)}\n"
                    f"Recovered (utf-8): {result_utf8}"
                )
                self.update_output(self.dec_output, output)
                self.show_success("Attack completed")

        except Exception as ex:
            self.show_error(f"Decryption failed: {ex}")

    def factorize_number(self):
        try:
            n_str = self.get_text_content(self.factor_n)
            if not self.validate_input(n_str, "Modulus (n)"):
                return
            try:
                n = int(n_str)
            except ValueError:
                self.show_error("n must be an integer")
                return

            # simple FactorDB printout; we show result in the output area
            # since factorize() prints to stdout, we will just inform the user
            factorize(n)
            self.update_output(self.factor_output, "Requested factorization. See console for FactorDB output.")
        except Exception as ex:
            self.show_error(f"Factorization failed: {ex}")

    def clear_encryption(self):
        try:
            self.enc_message.delete(1.0, tk.END)
        except Exception:
            self.enc_message.delete(0, tk.END)
        for widget in [self.enc_n, self.enc_e, self.enc_p, self.enc_flag_format]:
            widget.delete(0, tk.END)
        self.update_output(self.enc_output, "")

    def clear_decryption(self):
        for w in [
            self.dec_ciphertext,
            self.dec_n,
            self.dec_e,
            self.dec_p,
            self.dec_q,
            self.dec_c1,
            self.dec_c2,
            self.dec_e1,
            self.dec_e2,
            self.dec_n_common,
        ]:
            try:
                w.delete(1.0, tk.END)
            except Exception:
                w.delete(0, tk.END)
        self.update_output(self.dec_output, "")

    def clear_factorization(self):
        try:
            self.factor_n.delete(1.0, tk.END)
        except Exception:
            self.factor_n.delete(0, tk.END)
        self.update_output(self.factor_output, "")

    def _return_to_main(self):
        """Properly return to the main welcome screen"""
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