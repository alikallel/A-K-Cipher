import tkinter as tk
from tkinter import ttk
from gui.base_module import BaseGUIModule
from ROT.rot import rot_bruteforce


class ROTModule(BaseGUIModule):
    def __init__(self, parent, main_window=None):
        super().__init__(parent, "ROT")
        self.main_window = main_window

    def init_module(self):
        self.encryption_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.encryption_frame, text="Encryption")
        self.create_encryption_tab()

        self.decryption_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.decryption_frame, text="Decryption")
        self.create_decryption_tab()

        self.bruteforce_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.bruteforce_frame, text="Bruteforce")
        self.create_bruteforce_tab()

    def create_encryption_tab(self):
        input_frame = self.create_input_frame(self.encryption_frame, "ROT Encryption")
        
        self.enc_msg = self.create_text_input(input_frame, "Text:", multiline=True)
        self.enc_shift = self.create_text_input(input_frame, "ROT value (0-25):")

        btns = self.create_button_frame(input_frame)
        self.create_action_button(btns, "Encrypt", self.encrypt, 0)
        self.create_action_button(btns, "Clear", self.clear_encryption, 1)
        self.create_return_button(btns, self._return_to_main)

        output_frame = self.create_output_frame(self.encryption_frame, "Encryption Result")
        self.enc_output = self.create_output_text(output_frame)

    def create_decryption_tab(self):
        input_frame = self.create_input_frame(self.decryption_frame, "ROT Decryption")
        
        self.dec_msg = self.create_text_input(input_frame, "Ciphertext:", multiline=True)
        self.dec_shift = self.create_text_input(input_frame, "ROT value (0-25):")

        btns = self.create_button_frame(input_frame)
        self.create_action_button(btns, "Decrypt", self.decrypt, 0)
        self.create_action_button(btns, "Clear", self.clear_decryption, 1)
        self.create_return_button(btns, self._return_to_main)

        output_frame = self.create_output_frame(self.decryption_frame, "Decryption Result")
        self.dec_output = self.create_output_text(output_frame)

    def create_bruteforce_tab(self):
        input_frame = self.create_input_frame(self.bruteforce_frame, "ROT Bruteforce")
        
        self.bf_msg = self.create_text_input(input_frame, "Ciphertext:", multiline=True)

        btns = self.create_button_frame(input_frame)
        self.create_action_button(btns, "Bruteforce", self.bruteforce, 0)
        self.create_action_button(btns, "Clear", self.clear_bruteforce, 1)
        self.create_return_button(btns, self._return_to_main)

        output_frame = self.create_output_frame(self.bruteforce_frame, "Bruteforce Result")
        self.bf_output = self.create_output_text(output_frame)

    def _parse_shift(self, shift_widget):
        try:
            return int(shift_widget.get())
        except Exception:
            return None

    def _rot_transform(self, text: str, rot: int, encrypt: bool) -> str:
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                if encrypt:
                    result.append(chr((ord(char) - base + rot) % 26 + base))
                else:
                    result.append(chr((ord(char) - base - rot) % 26 + base))
            else:
                result.append(char)
        return ''.join(result)

    def encrypt(self):
        text = self.get_text_content(self.enc_msg)
        rot = self._parse_shift(self.enc_shift)
        if not self.validate_input(text, "Text") or rot is None:
            self.show_error("ROT must be an integer")
            return
        result = self._rot_transform(text, rot, True)
        self.update_output(self.enc_output, result)
        self.show_success("Encryption completed")

    def decrypt(self):
        text = self.get_text_content(self.dec_msg)
        rot = self._parse_shift(self.dec_shift)
        if not self.validate_input(text, "Text") or rot is None:
            self.show_error("ROT must be an integer")
            return
        result = self._rot_transform(text, rot, False)
        self.update_output(self.dec_output, result)
        self.show_success("Decryption completed")

    def bruteforce(self):
        text = self.get_text_content(self.bf_msg)
        if not self.validate_input(text, "Text"):
            return
        try:
            results = rot_bruteforce(text)
            lines = [f"ROT-{shift}: {decrypted}" for shift, decrypted in results]
            self.update_output(self.bf_output, "\n".join(lines))
            self.show_success("Bruteforce completed")
        except Exception as ex:
            self.show_error(f"Bruteforce failed: {ex}")

    def clear_encryption(self):
        try:
            self.enc_msg.delete(1.0, tk.END)
        except Exception:
            self.enc_msg.delete(0, tk.END)
        self.enc_shift.delete(0, tk.END)
        self.update_output(self.enc_output, "")

    def clear_decryption(self):
        try:
            self.dec_msg.delete(1.0, tk.END)
        except Exception:
            self.dec_msg.delete(0, tk.END)
        self.dec_shift.delete(0, tk.END)
        self.update_output(self.dec_output, "")

    def clear_bruteforce(self):
        try:
            self.bf_msg.delete(1.0, tk.END)
        except Exception:
            self.bf_msg.delete(0, tk.END)
        self.update_output(self.bf_output, "")

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