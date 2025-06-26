"""
UI components for dependency management.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, List, Optional, Tuple
import json
import os
import subprocess
import sys
from pathlib import Path

from .dependencies import DependencyResolver, PackageSpec
from .lang import tr

class DependencyDialog(tk.Toplevel):
    """Dialog for managing package dependencies."""
    
    def __init__(self, parent, project_path: str = None, on_install: Callable = None):
        """Initialize the dependency dialog.
        
        Args:
            parent: Parent window
            project_path: Path to the project (optional)
            on_install: Callback when dependencies are installed
        """
        super().__init__(parent)
        self.title(tr('dependencies'))
        self.parent = parent
        self.on_install = on_install
        self.project_path = project_path
        self.dependency_resolver = DependencyResolver()
        
        # Initialize package cache
        self.installed_packages = {}
        self.available_packages = {}
        
        self._create_widgets()
        self._load_dependencies()
        
        # Center the dialog
        self.transient(parent)
        self.grab_set()
        self.update_idletasks()
        width = 800
        height = 600
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create the dialog widgets."""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top frame for package info and actions
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Package name and version
        input_frame = ttk.LabelFrame(top_frame, text=tr('install_package'), padding=5)
        input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Label(input_frame, text=f"{tr('package_name')}:").grid(row=0, column=0, sticky=tk.W, padx=2, pady=2)
        self.pkg_name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.pkg_name_var).grid(
            row=0, column=1, sticky=tk.EW, padx=2, pady=2
        )
        
        ttk.Label(input_frame, text=f"{tr('package_version')}:").grid(row=0, column=2, sticky=tk.W, padx=2, pady=2)
        self.pkg_version_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.pkg_version_var, width=15).grid(
            row=0, column=3, sticky=tk.W, padx=2, pady=2
        )
        
        # Install options
        options_frame = ttk.Frame(input_frame)
        options_frame.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(5, 0))
        
        self.upgrade_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame, 
            text=tr('upgrade'),
            variable=self.upgrade_var
        ).pack(side=tk.LEFT, padx=2)
        
        self.force_reinstall_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame, 
            text=tr('force_reinstall'),
            variable=self.force_reinstall_var
        ).pack(side=tk.LEFT, padx=2)
        
        self.no_deps_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame, 
            text=tr('no_deps'),
            variable=self.no_deps_var
        ).pack(side=tk.LEFT, padx=2)
        
        self.pre_release_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame, 
            text=tr('pre_release'),
            variable=self.pre_release_var
        ).pack(side=tk.LEFT, padx=2)
        
        # Buttons
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Button(
            button_frame, 
            text=tr('install_btn'), 
            command=self._on_install,
            style='Accent.TButton',
            width=15
        ).pack(side=tk.TOP, fill=tk.X, pady=2)
        
        ttk.Button(
            button_frame, 
            text=tr('uninstall'), 
            command=self._on_uninstall,
            width=15
        ).pack(side=tk.TOP, fill=tk.X, pady=2)
        
        ttk.Button(
            button_frame, 
            text=tr('update'), 
            command=self._on_update,
            width=15
        ).pack(side=tk.TOP, fill=tk.X, pady=2)
        
        ttk.Button(
            button_frame, 
            text=tr('check_conflicts'), 
            command=self._on_check_conflicts,
            width=15
        ).pack(side=tk.TOP, fill=tk.X, pady=2)
        
        # Dependencies treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('package', 'version', 'required_by', 'status')
        self.tree = ttk.Treeview(
            tree_frame, 
            columns=columns, 
            show='headings',
            selectmode='extended'
        )
        
        # Configure columns
        self.tree.heading('package', text=tr('package'))
        self.tree.heading('version', text=tr('version'))
        self.tree.heading('required_by', text=tr('required_by'))
        self.tree.heading('status', text='Status')
        
        self.tree.column('package', width=200)
        self.tree.column('version', width=100, anchor=tk.CENTER)
        self.tree.column('required_by', width=200)
        self.tree.column('status', width=100, anchor=tk.CENTER)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        vsb.grid(row=0, column=1, sticky=tk.NS)
        hsb.grid(row=1, column=0, sticky=tk.EW)
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(
            main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self._on_selection_changed)
        self.pkg_name_var.trace_add('write', self._on_package_changed)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
    
    def _load_dependencies(self):
        """Load project dependencies."""
        self.status_var.set(tr('loading_dependencies') + '...')
        self.update()
        
        try:
            # Load installed packages
            self.installed_packages = self.dependency_resolver.get_installed_packages()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add installed packages to treeview
            for pkg, version in sorted(self.installed_packages.items()):
                self.tree.insert(
                    '', 
                    tk.END, 
                    values=(pkg, version, '', 'Installed'),
                    tags=('installed',)
                )
            
            # Try to load requirements from project
            if self.project_path:
                req_file = os.path.join(self.project_path, 'requirements.txt')
                if os.path.exists(req_file):
                    with open(req_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                try:
                                    spec = self.dependency_resolver.parse_requirement(line)
                                    if spec.name.lower() not in self.installed_packages:
                                        self.tree.insert(
                                            '', 
                                            tk.END, 
                                            values=(spec.name, spec.specifiers[0][1] if spec.specifiers else '', '', 'Not Installed'),
                                            tags=('not_installed',)
                                        )
                                except ValueError:
                                    continue
            
            # Configure tags
            self.tree.tag_configure('installed', foreground='green')
            self.tree.tag_configure('not_installed', foreground='red')
            
            self.status_var.set(tr('dependencies_loaded'))
            
        except Exception as e:
            messagebox.showerror(tr('error'), f"{tr('error_loading_dependencies')}: {str(e)}")
            self.status_var.set(tr('error_loading_dependencies'))
    
    def _on_selection_changed(self, event=None):
        """Handle selection changes in the treeview."""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            values = self.tree.item(item, 'values')
            if values:
                self.pkg_name_var.set(values[0])
                if len(values) > 1 and values[1]:
                    self.pkg_version_var.set(values[1])
    
    def _on_package_changed(self, *args):
        """Handle changes to the package name field."""
        pkg_name = self.pkg_name_var.get().strip()
        # TODO: Add package search/autocomplete
    
    def _on_install(self):
        """Handle install button click."""
        pkg_name = self.pkg_name_var.get().strip()
        if not pkg_name:
            messagebox.showwarning(tr('warning'), tr('no_package_selected'))
            return
        
        pkg_version = self.pkg_version_var.get().strip()
        if pkg_version:
            pkg_spec = f"{pkg_name}=={pkg_version}"
        else:
            pkg_spec = pkg_name
        
        # Build pip command
        cmd = [sys.executable, '-m', 'pip', 'install']
        
        if self.upgrade_var.get():
            cmd.append('--upgrade')
        if self.force_reinstall_var.get():
            cmd.append('--force-reinstall')
        if self.no_deps_var.get():
            cmd.append('--no-deps')
        if self.pre_release_var.get():
            cmd.append('--pre')
        
        cmd.append(pkg_spec)
        
        self._run_pip_command(cmd, tr('installing_dependencies'), tr('dependencies_installed'))
    
    def _on_uninstall(self):
        """Handle uninstall button click."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(tr('warning'), tr('no_package_selected'))
            return
        
        packages = []
        for item in selected:
            values = self.tree.item(item, 'values')
            if values:
                packages.append(values[0])
        
        if not packages:
            return
        
        if not messagebox.askyesno(
            tr('confirm_removal'),
            tr('confirm_uninstall_packages').format(packages=', '.join(packages))
        ):
            return
        
        cmd = [sys.executable, '-m', 'pip', 'uninstall', '-y'] + packages
        self._run_pip_command(cmd, tr('uninstalling_packages'), tr('packages_uninstalled'))
    
    def _on_update(self):
        """Handle update button click."""
        selected = self.tree.selection()
        if not selected:
            # Update all packages
            if not messagebox.askyesno(
                tr('confirm_update'),
                tr('confirm_update_all_packages')
            ):
                return
            
            cmd = [sys.executable, '-m', 'pip', 'install', '--upgrade']
            for item in self.tree.get_children():
                values = self.tree.item(item, 'values')
                if values and values[0].lower() != 'pip':  # Don't update pip itself
                    cmd.append(values[0])
            
            self._run_pip_command(cmd, tr('updating_packages'), tr('packages_updated'))
        else:
            # Update selected packages
            packages = []
            for item in selected:
                values = self.tree.item(item, 'values')
                if values and values[0].lower() != 'pip':  # Don't update pip itself
                    packages.append(values[0])
            
            if not packages:
                return
            
            cmd = [sys.executable, '-m', 'pip', 'install', '--upgrade'] + packages
            self._run_pip_command(cmd, tr('updating_packages'), tr('packages_updated'))
    
    def _on_check_conflicts(self):
        """Handle check conflicts button click."""
        self.status_var.set(tr('checking_conflicts'))
        self.update()
        
        try:
            # Get all requirements
            requirements = []
            for item in self.tree.get_children():
                values = self.tree.item(item, 'values')
                if values and values[3] == 'Installed':  # Only check installed packages
                    pkg_name = values[0]
                    pkg_version = values[1]
                    requirements.append(f"{pkg_name}=={pkg_version}" if pkg_version else pkg_name)
            
            # Check for conflicts
            conflicts = self.dependency_resolver.check_conflicts(requirements)
            
            if conflicts:
                conflict_msg = '\n'.join(f"- {pkg}: {reason}" for pkg, _, reason in conflicts)
                messagebox.showwarning(
                    tr('conflicts_found'),
                    f"{tr('conflicts_detected')}:\n\n{conflict_msg}"
                )
                self.status_var.set(tr('conflicts_found'))
            else:
                messagebox.showinfo(tr('no_conflicts'), tr('no_conflicts_found'))
                self.status_var.set(tr('no_conflicts'))
                
        except Exception as e:
            messagebox.showerror(tr('error'), f"{tr('error_checking_conflicts')}: {str(e)}")
            self.status_var.set(tr('error_checking_conflicts'))
    
    def _run_pip_command(self, cmd: list, progress_msg: str, success_msg: str):
        """Run a pip command and handle the result.
        
        Args:
            cmd: The command to run
            progress_msg: Message to show while running
            success_msg: Message to show on success
        """
        self.status_var.set(progress_msg)
        self.update()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Reload dependencies
            self._load_dependencies()
            
            # Show success message
            self.status_var.set(success_msg)
            
            # Call the on_install callback if provided
            if self.on_install:
                self.on_install()
                
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout or str(e)
            messagebox.showerror(
                tr('error'),
                f"{tr('error_executing_command')}:\n\n{error_msg}"
            )
            self.status_var.set(tr('error_executing_command'))
        except Exception as e:
            messagebox.showerror(
                tr('error'),
                f"{tr('unexpected_error')}: {str(e)}"
            )
            self.status_var.set(tr('error'))


class RequirementsDialog(tk.Toplevel):
    """Dialog for managing requirements.txt files."""
    
    def __init__(self, parent, project_path: str):
        """Initialize the requirements dialog.
        
        Args:
            parent: Parent window
            project_path: Path to the project
        """
        super().__init__(parent)
        self.title(tr('manage_requirements'))
        self.parent = parent
        self.project_path = project_path
        self.requirements_file = os.path.join(project_path, 'requirements.txt')
        
        self._create_widgets()
        self._load_requirements()
        
        # Center the dialog
        self.transient(parent)
        self.grab_set()
        self.update_idletasks()
        width = 600
        height = 400
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create the dialog widgets."""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text widget for editing requirements
        ttk.Label(main_frame, text=tr('requirements_file')).pack(anchor=tk.W)
        
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        self.text = tk.Text(text_frame, wrap=tk.WORD, undo=True)
        vsb = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text.yview)
        hsb = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.text.xview)
        self.text.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.text.grid(row=0, column=0, sticky=tk.NSEW)
        vsb.grid(row=0, column=1, sticky=tk.NS)
        hsb.grid(row=1, column=0, sticky=tk.EW)
        
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text=tr('save'),
            command=self._on_save,
            style='Accent.TButton'
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text=tr('cancel'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text=tr('install_requirements'),
            command=self._on_install_requirements
        ).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
    
    def _load_requirements(self):
        """Load requirements from requirements.txt."""
        if os.path.exists(self.requirements_file):
            with open(self.requirements_file, 'r') as f:
                self.text.delete('1.0', tk.END)
                self.text.insert('1.0', f.read())
    
    def _on_save(self):
        """Handle save button click."""
        try:
            with open(self.requirements_file, 'w') as f:
                f.write(self.text.get('1.0', tk.END))
            
            messagebox.showinfo(tr('success'), tr('requirements_saved'))
            self.destroy()
            
        except Exception as e:
            messagebox.showerror(tr('error'), f"{tr('error_saving_requirements')}: {str(e)}")
    
    def _on_install_requirements(self):
        """Handle install requirements button click."""
        # First save the requirements
        self._on_save()
        
        # Then install them
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', self.requirements_file],
                check=True,
                capture_output=True,
                text=True
            )
            
            messagebox.showinfo(tr('success'), tr('requirements_installed'))
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout or str(e)
            messagebox.showerror(
                tr('error'),
                f"{tr('error_installing_requirements')}:\n\n{error_msg}"
            )
        except Exception as e:
            messagebox.showerror(
                tr('error'),
                f"{tr('unexpected_error')}: {str(e)}"
            )
