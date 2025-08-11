"""
Main Window for A-K Cipher Tool GUI
"""
import tkinter as tk
from tkinter import ttk
import webbrowser
from gui.styles import Colors
from gui.rsa_module import RSAModule
from gui.xor_module import XORModule
from gui.caesar_module import CaesarModule
from gui.aes_module import AESModule
from gui.rot_module import ROTModule
from gui.base_encoding_module import BaseModule
from gui.dh_module import DHModule
from gui.math_module import MathModule


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.current_module = None

        # Remove icon setting from here; it should be set only once in app.py

        # Store reference to self in root for modules to access
        self.root.main_window = self

        self.main_frame = ttk.Frame(root, style='Main.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.create_header()
        self.create_navigation()  # Moved navigation after header
        self.create_content_area()
        self.show_welcome()

    def create_header(self):
        header_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))

        title_label = ttk.Label(header_frame, text="A-K Cipher Tool", style='Title.TLabel')
        title_label.pack()

        subtitle_label = ttk.Label(
            header_frame, text="Advanced Cryptography and Mathematics Toolkit", style='Info.TLabel'
        )
        subtitle_label.pack(pady=(5, 0))

        separator = ttk.Separator(header_frame, orient='horizontal')
        separator.pack(fill='x', pady=(10, 0))

    def create_navigation(self):
        self.nav_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        self.nav_frame.pack(fill='x', pady=(0, 20))  # Added bottom padding

        modules = [
            ("RSA", self.show_rsa),
            ("XOR Cipher", self.show_xor),
            ("Caesar Cipher", self.show_caesar),
            ("AES", self.show_aes),
            ("ROT", self.show_rot),
            ("Base Encoding", self.show_base),
            ("Diffie-Hellman", self.show_dh),
            ("Mathematics", self.show_math),
        ]

        for i, (name, command) in enumerate(modules):
            row = i // 4
            col = i % 4
            btn = ttk.Button(self.nav_frame, text=name, command=command, style='Action.TButton')
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')

        for i in range(4):
            self.nav_frame.columnconfigure(i, weight=1)

    def create_content_area(self):
        self.content_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        self.content_frame.pack(fill='both', expand=True)  # Removed bottom padding

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_module = None

    def hide_navigation(self):
        """Hide the navigation buttons"""
        if hasattr(self, 'nav_frame'):
            self.nav_frame.pack_forget()

    def show_navigation(self):
        """Show the navigation buttons"""
        if hasattr(self, 'nav_frame'):
            self.nav_frame.pack(fill='x', pady=(0, 20), before=self.content_frame)
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_module = None

    def open_github(self):
        """Open the GitHub repository in the default web browser"""
        try:
            webbrowser.open("https://github.com/alikallel/A-K-Cipher")
        except Exception:
            # If webbrowser fails, we could show a message with the URL
            pass

    def show_welcome(self):
        self.clear_content()
        self.show_navigation()  # Show navigation on welcome screen
        welcome_frame = ttk.Frame(self.content_frame, style='Main.TFrame')
        welcome_frame.pack(expand=True, fill='both')

        center_frame = ttk.Frame(welcome_frame, style='Main.TFrame')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Main welcome message
        welcome_label = ttk.Label(center_frame, text="Welcome to A-K Cipher Tool", style='Heading.TLabel')
        welcome_label.pack(pady=(0, 20))

        # Description and available modules
        info_text = (
            "The A-K Cipher Tool is a cryptographic toolkit designed for Capture The Flag (CTF) challenges and general cryptographic operations.\nThis tool supports multiple cipher techniques, including RSA, XOR, Caesar, AES, Diffie-Hellman, Base Encoding/Decoding, ROT ciphers, and advanced mathematical operations.\nIt also includes comprehensive mathematical tools for cryptanalysis, number theory transformations, and lattice operations."
        )
        info_label = ttk.Label(center_frame, text=info_text.strip(), style='Info.TLabel', justify='center')
        info_label.pack(pady=(0, 30))

        # GitHub section
        github_frame = ttk.Frame(center_frame, style='Main.TFrame')
        github_frame.pack(pady=(0, 20))

        github_text = ttk.Label(
            github_frame,
            text="If you find this tool useful, please consider giving us a star on GitHub!",
            style='Info.TLabel',
            justify='center'
        )
        github_text.pack(pady=(10, 15))

        # GitHub button
        github_btn = ttk.Button(
            github_frame,
            text="⭐ Star on GitHub",
            command=self.open_github,
            style='Action.TButton'
        )
        github_btn.pack()

    def show_rsa(self):
        self.clear_content()
        self.hide_navigation()  # Hide navigation when showing module
        self.current_module = RSAModule(self.content_frame, main_window=self)

    def show_xor(self):
        self.clear_content()
        self.hide_navigation()  # Hide navigation when showing module
        self.current_module = XORModule(self.content_frame, main_window=self)

    def show_caesar(self):
        self.clear_content()
        self.hide_navigation()  # Hide navigation when showing module
        self.current_module = CaesarModule(self.content_frame, main_window=self)

    def show_aes(self):
        self.clear_content()
        self.hide_navigation()  # Hide navigation when showing module
        self.current_module = AESModule(self.content_frame, main_window=self)

    def show_rot(self):
        self.clear_content()
        self.hide_navigation()  # Hide navigation when showing module
        self.current_module = ROTModule(self.content_frame, main_window=self)

    def show_base(self):
        self.clear_content()
        self.hide_navigation()  # Hide navigation when showing module
        self.current_module = BaseModule(self.content_frame, main_window=self)

    def show_dh(self):
        self.clear_content()
        self.hide_navigation()  # Hide navigation when showing module
        self.current_module = DHModule(self.content_frame, main_window=self)

    def show_math(self):
        self.clear_content()
        self.hide_navigation()  # Hide navigation when showing module
        self.current_module = MathModule(self.content_frame, main_window=self)