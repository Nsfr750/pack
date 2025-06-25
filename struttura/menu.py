import tkinter as tk
from tkinter import messagebox
import sys
import os

# Handle both direct execution and package import
try:
    from .about import About
    from .help import show_help
    from .sponsor import Sponsor
    from .log_viewer import LogViewer
    from .version import show_version
    from .lang import translator, tr, SUPPORTED_LANGUAGES
    from .updates import check_for_updates
except ImportError:
    # For direct execution
    from about import About
    from help import show_help
    from sponsor import Sponsor
    from log_viewer import LogViewer
    from version import show_version
    from lang import translator, tr, SUPPORTED_LANGUAGES
    from updates import check_for_updates

def create_menu_bar(root, app):
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label=tr('exit'), command=root.quit)
    menubar.add_cascade(label=tr('menu_file'), menu=file_menu)

    # Edit menu
    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label=tr('undo'), state='disabled')  # Will be connected to actual functionality
    edit_menu.add_command(label=tr('redo'), state='disabled')   # Will be connected to actual functionality
    edit_menu.add_separator()
    edit_menu.add_command(label=tr('cut'))
    edit_menu.add_command(label=tr('copy'))
    edit_menu.add_command(label=tr('paste'))
    edit_menu.add_command(label=tr('delete'))
    menubar.add_cascade(label=tr('menu_edit'), menu=edit_menu)

    # View menu
    view_menu = tk.Menu(menubar, tearoff=0)
    view_menu.add_checkbutton(label=tr('toolbar'))
    view_menu.add_checkbutton(label=tr('status_bar'))
    view_menu.add_checkbutton(label=tr('console'))
    view_menu.add_separator()
    view_menu.add_command(label=tr('zoom_in'))
    view_menu.add_command(label=tr('zoom_out'))
    view_menu.add_command(label=tr('reset_zoom'))
    menubar.add_cascade(label=tr('menu_view'), menu=view_menu)

    # Tools menu
    tools_menu = tk.Menu(menubar, tearoff=0)
    tools_menu.add_command(label=tr('package_manager'))
    tools_menu.add_separator()
    tools_menu.add_command(label=tr('view_log'), command=lambda: LogViewer.show_log(root))
    tools_menu.add_command(label=tr('terminal'))
    tools_menu.add_separator()
    tools_menu.add_command(label=tr('check_for_updates'), command=lambda: check_for_updates(root))
    menubar.add_cascade(label=tr('menu_tools'), menu=tools_menu)

    # Language menu
    def set_lang_and_restart(lang_code):
        if translator.set_language(lang_code):
            root.destroy()
            os.execl(sys.executable, sys.executable, *sys.argv)

    lang_menu = tk.Menu(menubar, tearoff=0)
    for code, label in SUPPORTED_LANGUAGES.items():
        lang_menu.add_command(
            label=label,
            command=lambda c=code: set_lang_and_restart(c)
        )
    menubar.add_cascade(label=tr('menu_language'), menu=lang_menu)

    # Help menu
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label=tr('documentation'), command=show_help)
    help_menu.add_command(label=tr('report_issue'))
    help_menu.add_separator()
    help_menu.add_command(label=tr('about'), command=lambda: About.show_about(root))
    help_menu.add_command(label=tr('sponsor'), command=lambda: Sponsor(root).show_sponsor())
    menubar.add_cascade(label=tr('menu_help'), menu=help_menu)

    return menubar


if __name__ == "__main__":
    # Test the menu
    root = tk.Tk()
    root.title("Menu Test")
    create_menu_bar(root, None)
    root.mainloop()
