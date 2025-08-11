import tkinter as tk
from tkinter import ttk
from gui.base_module import BaseGUIModule
from AES.aes128 import encrypt_aes_ecb, decrypt_aes_ecb, encrypt_aes_cbc, decrypt_aes_cbc


class AESModule(BaseGUIModule):
    def __init__(self, parent, main_window=None):
        super().__init__(parent, "AES")
        self.main_window = main_window

    def init_module(self):
        self.frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.frame, text="AES-128")
        self._build_tab(self.frame)

    def _build_tab(self, parent):
        input_frame = self.create_input_frame(parent, "AES Inputs")
        self.msg = self.create_text_input(input_frame, "Plaintext / Ciphertext (hex for decrypt):", multiline=True)
        self.key = self.create_text_input(input_frame, "Key (16 chars):")
        
        # Create mode selection frame similar to XOR format frame
        mode_frame = ttk.Frame(input_frame, style='Main.TFrame')
        mode_frame.pack(fill='x')
        ttk.Label(mode_frame, text="Mode:", style='Info.TLabel').pack(anchor='w')
        self.mode = ttk.Combobox(mode_frame, values=["ECB", "CBC"], state='readonly')
        self.mode.set("ECB")
        self.mode.pack(fill='x', pady=(0, 10))

        btns = self.create_button_frame(input_frame)
        self.create_action_button(btns, "Encrypt", self.encrypt, 0)
        self.create_action_button(btns, "Decrypt", self.decrypt, 1)
        self.create_action_button(btns, "Clear", self.clear, 2)
        self.create_return_button(btns, self._return_to_main)

        output_frame = self.create_output_frame(parent, "Output")
        self.output = self.create_output_text(output_frame)

    def encrypt(self):
        try:
            msg_text = self.get_text_content(self.msg)
            key_text = self.get_text_content(self.key)
            
            if not self.validate_input(msg_text, "Plaintext"):
                return
            if not self.validate_input(key_text, "Key"):
                return
                
            pt = msg_text.encode()
            key = key_text.encode()
            
            if len(key) != 16:
                self.show_error("AES key must be exactly 16 characters long.")
                return
                
            if self.mode.get() == 'ECB':
                ct = encrypt_aes_ecb(pt, key)
            else:
                ct = encrypt_aes_cbc(pt, key)
                
            self.update_output(self.output, ct.hex())
            self.show_success("Encryption completed")
        except Exception as ex:
            self.show_error(f"Encryption failed: {ex}")

    def decrypt(self):
        try:
            ct_hex = self.get_text_content(self.msg)
            key_text = self.get_text_content(self.key)
            
            if not self.validate_input(ct_hex, "Ciphertext"):
                return
            if not self.validate_input(key_text, "Key"):
                return
                
            key = key_text.encode()
            
            if len(key) != 16:
                self.show_error("AES key must be exactly 16 characters long.")
                return
                
            ct = bytes.fromhex(ct_hex)
            
            if self.mode.get() == 'ECB':
                pt = decrypt_aes_ecb(ct, key)
            else:
                pt = decrypt_aes_cbc(ct, key)
                
            self.update_output(self.output, pt.decode('utf-8', errors='ignore'))
            self.show_success("Decryption completed")
        except Exception as ex:
            self.show_error(f"Decryption failed: {ex}")

    def clear(self):
        try:
            self.msg.delete(1.0, tk.END)
        except Exception:
            self.msg.delete(0, tk.END)
        self.key.delete(0, tk.END)
        self.update_output(self.output, "")

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