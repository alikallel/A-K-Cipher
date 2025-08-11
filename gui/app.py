"""
GUI Main Application for A-K Cipher Tool
"""
import tkinter as tk
from tkinter import messagebox
from gui.main_window import MainWindow
from gui.styles import setup_styles
import sys
import os


class CipherToolGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("A-K Cipher Tool")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Set window icon using .ico for Windows compatibility (absolute path)
        ico_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./akwp.ico"))
        png_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./akwp.png"))
        try:
            self.root.iconbitmap(ico_path)
        except Exception:
            try:
                icon_img = tk.PhotoImage(file=png_path)
                self.root.iconphoto(True, icon_img)
            except Exception:
                pass  # Ignore if icon can't be set

        setup_styles(self.root)
        self.main_window = MainWindow(self.root)
        self.center_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit A-K Cipher Tool?"):
            self.root.destroy()
            sys.exit(0)

    def run(self):
        self.root.mainloop()


def main():
    try:
        app = CipherToolGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()


