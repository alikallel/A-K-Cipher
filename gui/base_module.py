"""
Base GUI Module - Abstract base class for cipher modules
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from abc import ABC, abstractmethod
from gui.styles import Colors


class BaseGUIModule(ABC):
    """Abstract base class for all cipher GUI modules."""

    def __init__(self, parent: tk.Misc, module_name: str):
        self.parent = parent
        self.module_name = module_name

        self.main_frame = ttk.Frame(parent, style='Main.TFrame')
        self.main_frame.pack(fill='both', expand=True)

        self.create_header()

        self.notebook = ttk.Notebook(self.main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, pady=(10, 0))

        self.init_module()

    def create_header(self):
        header_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        header_frame.pack(fill='x', pady=(0, 10))

        title_label = ttk.Label(header_frame, text=f"{self.module_name} Module", style='Heading.TLabel')
        title_label.pack()

        separator = ttk.Separator(header_frame, orient='horizontal')
        separator.pack(fill='x', pady=(5, 0))

    @abstractmethod
    def init_module(self):
        pass

    def create_input_frame(self, parent: tk.Misc, title: str = "Input") -> ttk.LabelFrame:
        frame = ttk.LabelFrame(parent, text=title, padding=10)
        frame.pack(fill='x', pady=(0, 10))
        return frame

    def create_output_frame(self, parent: tk.Misc, title: str = "Output") -> ttk.LabelFrame:
        frame = ttk.LabelFrame(parent, text=title, padding=10)
        frame.pack(fill='both', expand=True, pady=(0, 10))
        return frame

    def create_text_input(self, parent: tk.Misc, label: str, multiline: bool = False, height: int = 3):
        label_widget = ttk.Label(parent, text=label, style='Info.TLabel')
        label_widget.pack(anchor='w', pady=(0, 5))

        if multiline:
            text_widget = scrolledtext.ScrolledText(
                parent,
                height=height,
                wrap=tk.WORD,
                bg=Colors.ENTRY_BG,
                fg=Colors.FOREGROUND,
                insertbackground=Colors.FOREGROUND,
                selectbackground=Colors.SELECT_BG,
                selectforeground=Colors.SELECT_FG,
            )
            text_widget.pack(fill='x', pady=(0, 10))
            return text_widget
        entry = ttk.Entry(parent, style='Custom.TEntry', font=('Consolas', 10))
        entry.pack(fill='x', pady=(0, 10))
        return entry

    def create_combobox(self, parent: tk.Misc, label: str, values, default=None) -> ttk.Combobox:
        label_widget = ttk.Label(parent, text=label, style='Info.TLabel')
        label_widget.pack(anchor='w', pady=(0, 5))

        combo = ttk.Combobox(parent, values=values, state='readonly', style='Custom.TCombobox')
        combo.pack(fill='x', pady=(0, 10))

        if default is not None:
            combo.set(default)
        elif values:
            combo.set(values[0])
        return combo

    def create_button_frame(self, parent: tk.Misc) -> ttk.Frame:
        button_frame = ttk.Frame(parent, style='Main.TFrame')
        button_frame.pack(fill='x', pady=(10, 0))
        return button_frame

    def create_action_button(self, parent: ttk.Frame, text: str, command, column: int = 0) -> ttk.Button:
        btn = ttk.Button(parent, text=text, command=command, style='Action.TButton')
        btn.grid(row=0, column=column, padx=5, sticky='ew')
        parent.columnconfigure(column, weight=1)
        return btn

    def create_output_text(self, parent: tk.Misc, height: int = 10) -> scrolledtext.ScrolledText:
        text_widget = scrolledtext.ScrolledText(
            parent,
            height=height,
            wrap=tk.WORD,
            bg=Colors.ENTRY_BG,
            fg=Colors.FOREGROUND,
            insertbackground=Colors.FOREGROUND,
            selectbackground=Colors.SELECT_BG,
            selectforeground=Colors.SELECT_FG,
            state='disabled',
        )
        text_widget.pack(fill='both', expand=True)
        return text_widget

    def update_output(self, text_widget: scrolledtext.ScrolledText, content: str, clear: bool = True):
        text_widget.config(state='normal')
        if clear:
            text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, content)
        text_widget.config(state='disabled')
        text_widget.see(tk.END)

    def show_error(self, message: str):
        messagebox.showerror("Error", message)

    def show_success(self, message: str):
        messagebox.showinfo("Success", message)

    def show_warning(self, message: str):
        messagebox.showwarning("Warning", message)

    def create_return_button(self, parent: ttk.Frame, on_return):
        """Add a Return button to go back to the main page."""
        btn = ttk.Button(parent, text="Return", command=on_return, style='Action.TButton')
        # Place to the far right by giving it a high column index
        col = 3
        btn.grid(row=0, column=col, padx=5, sticky='ew')
        for i in range(col + 1):
            parent.columnconfigure(i, weight=1)
        return btn

    def get_text_content(self, text_widget):
        if isinstance(text_widget, scrolledtext.ScrolledText):
            return text_widget.get(1.0, tk.END).strip()
        return text_widget.get().strip()

    def validate_input(self, value: str, field_name: str, required: bool = True) -> bool:
        if required and not value:
            self.show_error(f"{field_name} is required")
            return False
        return True

    def clear_outputs(self, *text_widgets):
        for widget in text_widgets:
            self.update_output(widget, "")


