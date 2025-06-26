import tkinter as tk
from tkinter import ttk, messagebox
from .lang import tr

class Help:
    
    @staticmethod
    def show_help(parent):
        """
        Display the Help dialog.
        
        This method creates and shows a modal dialog with help information
        organized in tabs. The dialog includes sections for usage instructions,
        features, and tips.
        
        Args:
            parent (tk.Tk): The parent window for the dialog
        """
        # Create and configure the help window
        help_window = tk.Toplevel(parent)
        help_window.title(tr('help'))
        help_window.geometry("700x500")
        help_window.minsize(600, 400)
        
        # Center the window on screen
        window_width = 700
        window_height = 500
        screen_width = help_window.winfo_screenwidth()
        screen_height = help_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        help_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(help_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== USAGE TAB =====
        usage_frame = ttk.Frame(notebook, padding=10)
        notebook.add(usage_frame, text=tr('usage_tab'))
        usage_text = tr('help_usage')
        usage_label = tk.Label(usage_frame, text=usage_text, justify=tk.LEFT, anchor='nw', wraplength=650)
        usage_label.pack(fill=tk.BOTH, expand=True)

        # ===== FEATURES TAB =====
        features_frame = ttk.Frame(notebook, padding=10)
        notebook.add(features_frame, text=tr('features_tab'))
        features_text = tr('help_features')
        features_label = tk.Label(features_frame, text=features_text, justify=tk.LEFT, anchor='nw', wraplength=650)
        features_label.pack(fill=tk.BOTH, expand=True)

        # Close button
        close_btn = tk.Button(help_window, text=tr('close'), command=help_window.destroy)
        close_btn.pack(pady=10)
        
        # Make the window modal
        help_window.transient(parent)
        help_window.grab_set()
        parent.wait_window(help_window)
