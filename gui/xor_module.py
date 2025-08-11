import tkinter as tk
from tkinter import ttk
from gui.base_module import BaseGUIModule
from XOR.encrypt import xor_encrypt_normal
from XOR.decrypt import xor_decrypt_normal


class XORModule(BaseGUIModule):
    def __init__(self, parent, main_window=None):
        super().__init__(parent, "XOR Cipher")
        self.main_window = main_window

    def init_module(self):
        self.encryption_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.encryption_frame, text="Encryption")
        self.create_encryption_tab()

        self.decryption_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.decryption_frame, text="Decryption")
        self.create_decryption_tab()

    def create_encryption_tab(self):
        input_frame = self.create_input_frame(self.encryption_frame, "XOR Encryption")

        self.enc_msg = self.create_text_input(input_frame, "Message:", multiline=True)
        self.enc_key = self.create_text_input(input_frame, "Key:")
        self.enc_flag_format = self.create_text_input(input_frame, "Flag Format (optional):")

        btns = self.create_button_frame(input_frame)
        self.create_action_button(btns, "Encrypt", self.encrypt, 0)
        self.create_action_button(btns, "Clear", self.clear_encryption, 1)
        self.create_return_button(btns, self._return_to_main)

        output_frame = self.create_output_frame(self.encryption_frame, "Encryption Result")
        self.enc_output = self.create_output_text(output_frame)

    def create_decryption_tab(self):
        input_frame = self.create_input_frame(self.decryption_frame, "XOR Decryption")

        self.dec_msg = self.create_text_input(input_frame, "Ciphertext:", multiline=True)
        self.dec_key = self.create_text_input(input_frame, "Key:")

        fmt_frame = ttk.Frame(input_frame, style='Main.TFrame')
        fmt_frame.pack(fill='x')
        ttk.Label(fmt_frame, text="Ciphertext format:", style='Info.TLabel').pack(anchor='w')
        self.dec_input_format = ttk.Combobox(fmt_frame, values=["Raw", "Hex"], state='readonly')
        self.dec_input_format.set("Hex")
        self.dec_input_format.pack(fill='x', pady=(0, 10))

        btns = self.create_button_frame(input_frame)
        self.create_action_button(btns, "Decrypt", self.decrypt, 0)
        self.create_action_button(btns, "Clear", self.clear_decryption, 1)
        self.create_return_button(btns, self._return_to_main)

        output_frame = self.create_output_frame(self.decryption_frame, "Decryption Result")
        self.dec_output = self.create_output_text(output_frame)

    def encrypt(self):
        try:
            message = self.get_text_content(self.enc_msg)
            key = self.get_text_content(self.enc_key)
            flag = self.get_text_content(self.enc_flag_format)
            if not self.validate_input(message, "Message") or not self.validate_input(key, "Key"):
                return
            ct = xor_encrypt_normal(message, key, flag or None)
            out = f"Hex: {ct.hex()}\nRaw: {ct}"
            self.update_output(self.enc_output, out)
            self.show_success("XOR encryption complete")
        except Exception as ex:
            self.show_error(f"Encryption failed: {ex}")

    def decrypt(self):
        try:
            data = self.get_text_content(self.dec_msg)
            key = self.get_text_content(self.dec_key)
            fmt = self.dec_input_format.get()
            if not self.validate_input(data, "Ciphertext") or not self.validate_input(key, "Key"):
                return
            if fmt == "Hex":
                pt = xor_decrypt_normal(data, key)
            else:
                pt = xor_decrypt_normal(data.encode('utf-8'), key)
            out = f"UTF-8: {pt.decode('utf-8', errors='ignore')}\nHex: {pt.hex()}\nRaw: {pt}"
            self.update_output(self.dec_output, out)
            self.show_success("XOR decryption complete")
        except Exception as ex:
            self.show_error(f"Decryption failed: {ex}")

    def clear_encryption(self):
        try:
            self.enc_msg.delete(1.0, tk.END)
        except Exception:
            self.enc_msg.delete(0, tk.END)
        for w in [self.enc_key, self.enc_flag_format]:
            w.delete(0, tk.END)
        self.update_output(self.enc_output, "")

    def clear_decryption(self):
        try:
            self.dec_msg.delete(1.0, tk.END)
        except Exception:
            self.dec_msg.delete(0, tk.END)
        self.dec_key.delete(0, tk.END)
        self.update_output(self.dec_output, "")

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