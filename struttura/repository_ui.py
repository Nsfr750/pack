"""
UI components for repository management.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, Dict, List
from .repository import RepositoryManager, PackageRepository
from .lang import tr

class RepositoryDialog(tk.Toplevel):
    """Dialog for adding/editing a repository."""
    
    def __init__(self, parent, repository: PackageRepository = None, on_save: Callable = None):
        """Initialize the dialog.
        
        Args:
            parent: Parent window
            repository: Optional repository to edit
            on_save: Callback when repository is saved
        """
        super().__init__(parent)
        self.title(tr('edit_repository') if repository else tr('add_repository'))
        self.parent = parent
        self.on_save = on_save
        self.repository = repository or PackageRepository('', '')
        
        self._create_widgets()
        self._populate_fields()
        
        # Center the dialog
        self.transient(parent)
        self.grab_set()
        self.update_idletasks()
        width = 400
        height = 250
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create the dialog widgets."""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name
        ttk.Label(main_frame, text=f"{tr('name')}:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var).grid(
            row=0, column=1, sticky=tk.EW, padx=5, pady=2
        )
        
        # URL
        ttk.Label(main_frame, text="URL:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.url_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.url_var).grid(
            row=1, column=1, sticky=tk.EW, padx=5, pady=2
        )
        
        # Username
        ttk.Label(main_frame, text=f"{tr('username')} (optional):").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        self.username_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.username_var).grid(
            row=2, column=1, sticky=tk.EW, padx=5, pady=2
        )
        
        # Password
        ttk.Label(main_frame, text=f"{tr('password')} (optional):").grid(
            row=3, column=0, sticky=tk.W, pady=2
        )
        self.password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.password_var, show="*").grid(
            row=3, column=1, sticky=tk.EW, padx=5, pady=2
        )
        
        # Default checkbox
        self.default_var = tk.BooleanVar(value=self.repository.is_default)
        ttk.Checkbutton(
            main_frame, 
            text=tr('set_as_default'),
            variable=self.default_var
        ).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky=tk.E)
        
        ttk.Button(
            button_frame, 
            text=tr('cancel'), 
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame, 
            text=tr('save'), 
            command=self._on_save,
            style='Accent.TButton'
        ).pack(side=tk.RIGHT, padx=5)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
        # Bind Enter key to save
        self.bind('<Return>', lambda e: self._on_save())
    
    def _populate_fields(self):
        """Populate the form fields with repository data."""
        if self.repository:
            self.name_var.set(self.repository.name)
            self.url_var.set(self.repository.url)
            self.username_var.set(self.repository.username or '')
            # Don't pre-fill password for security
    
    def _on_save(self):
        """Handle save button click."""
        name = self.name_var.get().strip()
        url = self.url_var.get().strip()
        username = self.username_var.get().strip() or None
        password = self.password_var.get() or None
        is_default = self.default_var.get()
        
        if not name:
            messagebox.showerror(tr('error'), tr('name_required'))
            return
            
        if not url:
            messagebox.showerror(tr('error'), tr('url_required'))
            return
        
        # Create/update the repository
        self.repository = PackageRepository(
            name=name,
            url=url,
            username=username,
            password=password,
            is_default=is_default
        )
        
        if self.on_save:
            self.on_save(self.repository)
        
        self.destroy()


class RepositoryManagerFrame(ttk.Frame):
    """Frame for managing package repositories."""
    
    def __init__(self, parent, repository_manager, **kwargs):
        """Initialize the repository manager frame.
        
        Args:
            parent: Parent widget
            repository_manager: RepositoryManager instance
        """
        super().__init__(parent, **kwargs)
        self.repository_manager = repository_manager
        self._create_widgets()
        self._load_repositories()
    
    def _create_widgets(self):
        """Create the UI widgets."""
        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            toolbar, 
            text=tr('add_repository'),
            command=self._on_add_repository,
            style='Accent.TButton'
        ).pack(side=tk.LEFT, padx=2)
        
        self.edit_btn = ttk.Button(
            toolbar,
            text=tr('edit_repository'),
            command=self._on_edit_repository,
            state=tk.DISABLED
        )
        self.edit_btn.pack(side=tk.LEFT, padx=2)
        
        self.remove_btn = ttk.Button(
            toolbar,
            text=tr('remove_repository'),
            command=self._on_remove_repository,
            state=tk.DISABLED
        )
        self.remove_btn.pack(side=tk.LEFT, padx=2)
        
        self.set_default_btn = ttk.Button(
            toolbar,
            text=tr('set_as_default'),
            command=self._on_set_default,
            state=tk.DISABLED
        )
        self.set_default_btn.pack(side=tk.LEFT, padx=2)
        
        # Repositories list
        columns = ('name', 'url', 'auth', 'default')
        self.tree = ttk.Treeview(
            self, 
            columns=columns, 
            show='headings',
            selectmode='browse'
        )
        
        # Configure columns
        self.tree.heading('name', text=tr('name'))
        self.tree.heading('url', text='URL')
        self.tree.heading('auth', text=tr('authentication'))
        self.tree.heading('default', text=tr('default'))
        
        self.tree.column('name', width=150)
        self.tree.column('url', width=300)
        self.tree.column('auth', width=100, anchor=tk.CENTER)
        self.tree.column('default', width=80, anchor=tk.CENTER)
        
        # Add scrollbar
        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Pack everything
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self._on_selection_changed)
    
    def _load_repositories(self):
        """Load repositories into the treeview."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add repositories
        for repo in self.repository_manager.list_repositories():
            self.tree.insert('', tk.END, values=(
                repo.name,
                repo.url,
                '✓' if repo.username else '',
                '✓' if repo.is_default else ''
            ), tags=('default' if repo.is_default else '',))
        
        # Update button states
        self._update_button_states()
    
    def _on_selection_changed(self, event=None):
        """Handle selection changes in the treeview."""
        self._update_button_states()
    
    def _update_button_states(self):
        """Update the state of action buttons based on selection."""
        selected = bool(self.tree.selection())
        self.edit_btn.config(state=tk.NORMAL if selected else tk.DISABLED)
        self.remove_btn.config(state=tk.NORMAL if selected else tk.DISABLED)
        self.set_default_btn.config(state=tk.NORMAL if selected else tk.DISABLED)
    
    def _on_add_repository(self):
        """Handle add repository button click."""
        def on_save(repo):
            self.repository_manager.add_repository(repo)
            self._load_repositories()
        
        dialog = RepositoryDialog(self, on_save=on_save)
        dialog.wait_window()
    
    def _on_edit_repository(self):
        """Handle edit repository button click."""
        selected = self.tree.selection()
        if not selected:
            return
            
        item = selected[0]
        repo_name = self.tree.item(item, 'values')[0]
        repo = self.repository_manager.get_repository(repo_name)
        
        if not repo:
            messagebox.showerror(tr('error'), tr('repository_not_found'))
            return
        
        def on_save(updated_repo):
            self.repository_manager.add_repository(updated_repo)
            self._load_repositories()
        
        dialog = RepositoryDialog(self, repo, on_save=on_save)
        dialog.wait_window()
    
    def _on_remove_repository(self):
        """Handle remove repository button click."""
        selected = self.tree.selection()
        if not selected:
            return
            
        item = selected[0]
        repo_name = self.tree.item(item, 'values')[0]
        
        if messagebox.askyesno(
            tr('confirm_removal'),
            tr('confirm_remove_repository').format(name=repo_name)
        ):
            if self.repository_manager.remove_repository(repo_name):
                self._load_repositories()
    
    def _on_set_default(self):
        """Handle set as default button click."""
        selected = self.tree.selection()
        if not selected:
            return
            
        item = selected[0]
        repo_name = self.tree.item(item, 'values')[0]
        
        if self.repository_manager.set_default_repository(repo_name):
            self._load_repositories()
