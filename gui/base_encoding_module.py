import tkinter as tk
from tkinter import ttk
from gui.base_module import BaseGUIModule
from Base.base64ed import encode_base64, decode_base64
from Base.base32ed import encode_base32, decode_base32
from Base.base16ed import encode_base16, decode_base16


class BaseModule(BaseGUIModule):
    def __init__(self, parent, main_window=None):
        super().__init__(parent, "Base Encoding")
        self.main_window = main_window

    def init_module(self):
        self.frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.frame, text="Base Encodings")
        self._build_tab(self.frame)

    def _build_tab(self, parent):
        input_frame = self.create_input_frame(parent, "Inputs")
        self.msg = self.create_text_input(input_frame, "Text:", multiline=True)
        
        # Create base selection frame similar to XOR format frame
        base_frame = ttk.Frame(input_frame, style='Main.TFrame')
        base_frame.pack(fill='x')
        ttk.Label(base_frame, text="Base:", style='Info.TLabel').pack(anchor='w')
        self.base = ttk.Combobox(base_frame, values=["Base64", "Base32", "Base16"], state='readonly')
        self.base.set("Base64")
        self.base.pack(fill='x', pady=(0, 10))
        
        # Create operation selection frame similar to XOR format frame
        mode_frame = ttk.Frame(input_frame, style='Main.TFrame')
        mode_frame.pack(fill='x')
        ttk.Label(mode_frame, text="Operation:", style='Info.TLabel').pack(anchor='w')
        self.mode = ttk.Combobox(mode_frame, values=["Encode", "Decode"], state='readonly')
        self.mode.set("Encode")
        self.mode.pack(fill='x', pady=(0, 10))

        btns = self.create_button_frame(input_frame)
        self.create_action_button(btns, "Process", self.process, 0)
        self.create_action_button(btns, "Clear", self.clear, 1)
        self.create_return_button(btns, self._return_to_main)

        output_frame = self.create_output_frame(parent, "Output")
        self.output = self.create_output_text(output_frame)

    def process(self):
        try:
            text = self.get_text_content(self.msg)
            if not self.validate_input(text, "Text"):
                return
                
            op = self.mode.get()
            base = self.base.get()
            
            if base == "Base64":
                result = encode_base64(text) if op == "Encode" else decode_base64(text)
            elif base == "Base32":
                result = encode_base32(text) if op == "Encode" else decode_base32(text)
            else:  # Base16
                result = encode_base16(text) if op == "Encode" else decode_base16(text)
                
            self.update_output(self.output, str(result))
            self.show_success(f"{op} completed using {base}")
        except Exception as ex:
            self.show_error(f"Processing failed: {ex}")

    def clear(self):
        try:
            self.msg.delete(1.0, tk.END)
        except Exception:
            self.msg.delete(0, tk.END)
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