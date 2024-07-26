from tkinter import ttk
from config import CONFIG

def setup_styles() -> None:
    """
    Setup the styles for the application using the configuration settings.
    """
    style = ttk.Style()
    style.theme_use('clam')
    
    # General styles
    style.configure("TFrame", background=CONFIG['bg_color'])
    style.configure("TLabel", background=CONFIG['bg_color'], foreground="white")
    style.configure("TEntry", fieldbackground=CONFIG['input_bg'], foreground="white", insertcolor="white")
    style.configure("TButton", background=CONFIG['add_button_bg'], foreground="white")
    style.map("TButton", background=[('active', CONFIG['add_button_active_bg'])])
    
    # Specific styles
    style.configure("Done.TCheckbutton", background=CONFIG['bg_color'])
    style.configure("New.TLabel", background=CONFIG['new_task_bg'], foreground="white", padding=(5, 2))
    style.configure("Done.TLabel", background=CONFIG['done_task_bg'], foreground="white", padding=(5, 2))
    style.configure("Remove.TButton", background=CONFIG['bg_color'], foreground="red")
