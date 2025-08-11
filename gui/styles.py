"""
GUI Styles and Theme Configuration
"""
import tkinter as tk
from tkinter import ttk


def setup_styles(root: tk.Tk):
    """Set up custom styles for the application."""

    root.configure(bg='#1a1a1a')

    style = ttk.Style(root)

    try:
        style.theme_use('clam')
    except Exception:
        style.theme_use('default')

    colors = {
        'bg': '#1a1a1a',
        'fg': '#e0e0e0',
        'select_bg': '#333333',
        'select_fg': '#00ff88',
        'button_bg': '#2d2d2d',
        'button_hover': '#3a3a3a',
        'entry_bg': '#242424',
        'frame_bg': '#1f1f1f',
    }

    style.configure('Main.TFrame', background=colors['bg'], borderwidth=0)

    style.configure(
        'Action.TButton',
        background=colors['button_bg'],
        foreground=colors['fg'],
        borderwidth=1,
        focuscolor='none',
        padding=(10, 8),
    )
    style.map(
        'Action.TButton',
        background=[('active', colors['button_hover']), ('pressed', colors['select_bg'])],
        foreground=[('active', colors['fg'])],
    )

    style.configure('Title.TLabel', background=colors['bg'], foreground=colors['select_fg'], font=('Arial', 16, 'bold'))
    style.configure('Heading.TLabel', background=colors['bg'], foreground=colors['fg'], font=('Arial', 12, 'bold'))
    style.configure('Info.TLabel', background=colors['bg'], foreground=colors['fg'], font=('Arial', 10))

    style.configure(
        'Custom.TEntry',
        fieldbackground=colors['entry_bg'],
        background=colors['entry_bg'],
        foreground=colors['fg'],
        borderwidth=1,
        insertcolor=colors['fg'],
    )

    style.configure(
        'Custom.TText',
        fieldbackground=colors['entry_bg'],
        background=colors['entry_bg'],
        foreground=colors['fg'],
        borderwidth=1,
        insertcolor=colors['fg'],
    )

    style.configure('Custom.TNotebook', background=colors['bg'], borderwidth=0)
    style.configure(
        'Custom.TNotebook.Tab',
        background=colors['button_bg'],
        foreground=colors['fg'],
        padding=(12, 8),
        borderwidth=1,
    )
    style.map(
        'Custom.TNotebook.Tab',
        background=[('selected', colors['select_bg']), ('active', colors['button_hover'])],
        foreground=[('selected', colors['fg']), ('active', colors['fg'])],
    )

    style.configure(
        'Custom.TCombobox',
        fieldbackground=colors['entry_bg'],
        background=colors['entry_bg'],
        foreground=colors['fg'],
        borderwidth=1,
        selectbackground=colors['select_bg'],
        selectforeground=colors['fg'],
    )

    style.configure(
        'Custom.Vertical.TScrollbar',
        background=colors['button_bg'],
        troughcolor=colors['bg'],
        borderwidth=1,
        arrowcolor=colors['fg'],
    )

    # LabelFrame styling for dark mode
    style.configure(
        'TLabelframe',
        background=colors['bg'],
        foreground=colors['fg'],
        borderwidth=1,
        relief='solid',
    )
    
    style.configure(
        'TLabelframe.Label',
        background=colors['bg'],
        foreground=colors['select_fg'],
        font=('Arial', 10, 'bold'),
    )

    return colors


class Colors:
    """Color constants for the application."""
    BACKGROUND = '#1a1a1a'
    FOREGROUND = '#e0e0e0'
    SELECT_BG = '#333333'
    SELECT_FG = '#00ff88'
    BUTTON_BG = '#2d2d2d'
    BUTTON_HOVER = '#3a3a3a'
    ENTRY_BG = '#242424'
    FRAME_BG = '#1f1f1f'
    ERROR = '#ff4444'
    SUCCESS = '#44ff44'
    WARNING = '#ffaa44'