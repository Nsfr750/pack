import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import subprocess
import os
import sys
import json
import platform
import shutil
import webbrowser
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable

# Local imports
from struttura.menu import create_menu_bar
from struttura.lang import tr
from struttura.templates import template_manager, PackageTemplate
from struttura.repository import RepositoryManager, PackageRepository
from struttura.repository_ui import RepositoryManagerFrame, RepositoryDialog
from struttura.dependency_ui import DependencyDialog, RequirementsDialog
from struttura.dependencies import DependencyResolver


class NewProjectDialog(tk.Toplevel):
    """Dialog for creating a new project from a template."""
    
    def __init__(self, parent, on_create):
        super().__init__(parent)
        self.title(tr("new_project"))
        self.parent = parent
        self.on_create = on_create
        self.result = None
        
        # Center the dialog
        self.geometry("500x400")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._center_on_parent()
    
    def _center_on_parent(self):
        """Center the dialog on the parent window."""
        self.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()
        
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Create the dialog widgets."""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Project name
        ttk.Label(main_frame, text=tr("project_name") + ":").pack(anchor=tk.W, pady=(0, 5))
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var).pack(fill=tk.X, pady=(0, 10))
        
        # Project location
        ttk.Label(main_frame, text=tr("location") + ":").pack(anchor=tk.W, pady=(0, 5))
        
        loc_frame = ttk.Frame(main_frame)
        loc_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.loc_var = tk.StringVar(value=str(Path.home() / "Projects"))
        ttk.Entry(loc_frame, textvariable=self.loc_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(
            loc_frame, 
            text=tr("browse"), 
            command=self._browse_location,
            width=10
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Template selection
        ttk.Label(main_frame, text=tr("template") + ":").pack(anchor=tk.W, pady=(0, 5))
        
        self.template_var = tk.StringVar()
        self.template_listbox = tk.Listbox(main_frame, height=8)
        self.template_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Add templates to listbox
        self.templates = {}
        for template in template_manager.list_templates():
            self.templates[template['name']] = template
            self.template_listbox.insert(tk.END, f"{template['name']} - {template['description']}")
        
        # Select first template by default
        if self.template_listbox.size() > 0:
            self.template_listbox.selection_set(0)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            btn_frame, 
            text=tr("create"), 
            command=self._on_create,
            style="Accent.TButton"
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(
            btn_frame, 
            text=tr("cancel"), 
            command=self.destroy
        ).pack(side=tk.RIGHT)
    
    def _browse_location(self):
        """Open a directory selection dialog."""
        path = filedialog.askdirectory(
            initialdir=self.loc_var.get(),
            title=tr("select_directory")
        )
        if path:
            self.loc_var.set(path)
    
    def _on_create(self):
        """Handle create button click."""
        name = self.name_var.get().strip()
        location = self.loc_var.get().strip()
        
        if not name:
            messagebox.showerror(tr("error"), tr("project_name_required"))
            return
            
        if not location:
            messagebox.showerror(tr("error"), tr("location_required"))
            return
            
        # Get selected template
        selection = self.template_listbox.curselection()
        if not selection:
            messagebox.showerror(tr("error"), tr("template_required"))
            return
            
        template_name = list(self.templates.keys())[selection[0]]
        
        # Create project directory
        project_path = os.path.join(location, name)
        
        try:
            # Create the project from template
            success = template_manager.create_from_template(
                template_name=template_name,
                path=location,
                package_name=name.replace(" ", "_").lower(),
                project_name=name
            )
            
            if success:
                self.result = project_path
                self.destroy()
            else:
                messagebox.showerror(
                    tr("error"),
                    tr("project_creation_failed").format(path=project_path)
                )
                
        except Exception as e:
            messagebox.showerror(
                tr("error"),
                tr("project_creation_error").format(error=str(e))
            )
    
    def show(self) -> Optional[str]:
        """Show the dialog and return the result."""
        self.wait_window()
        return self.result


class PyPackagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(tr("app_title"))
        self.style = ttk.Style()
        
        # Set theme if available
        try:
            import ttkthemes
            # Try to use arc theme, fall back to default if not available
            try:
                self.style.theme_use('arc')
            except tk.TclError:
                # Fall back to default theme if arc is not available
                available_themes = self.style.theme_names()
                if available_themes:
                    self.style.theme_use(available_themes[0])
        except ImportError:
            pass  # Use default theme if ttkthemes is not installed
        
        # Initialize managers
        self.repository_manager = RepositoryManager()
        self.dependency_resolver = DependencyResolver()
        
        # Create menu
        self.menubar = create_menu_bar(self.root, self)
        
        # Configure window
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.minsize(1000, 700)
        
        # Initialize variables
        self.current_project = None
        self.project_path = None
        
        # Create UI
        self.create_widgets()
        
        # Initialize settings
        self.settings = {
            'recent_projects': [],
            'window_geometry': '1000x700',
            'theme': 'default',
            'language': 'en',
            'python_path': sys.executable,
            'venv_path': '',
            'last_project': ''
        }
        
        # Load settings from file
        self.load_settings()
        
    def create_widgets(self):
        """Create the main application widgets."""
        # Main container - using tk.PanedWindow for better control
        self.main_container = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=5, sashrelief=tk.RAISED)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar frame with fixed width
        self.sidebar = ttk.Frame(self.main_container, width=200, style='Sidebar.TFrame')
        self.main_container.add(self.sidebar, minsize=150, width=200)
        
        # Create content frame that takes remaining space
        self.content = ttk.Frame(self.main_container)
        self.main_container.add(self.content, minsize=400)
        
        # Configure the paned window panes using the actual frame widgets
        self.main_container.paneconfigure(self.sidebar, minsize=150, width=200)
        self.main_container.paneconfigure(self.content, minsize=400)
        
        # Create sidebar buttons
        self._create_sidebar()
        
        # Create content area
        self._create_content_area()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var.set(tr('ready'))
    
    def _create_content_area(self):
        """Create the main content area."""
        # Welcome message
        welcome_label = ttk.Label(
            self.content,
            text=tr('welcome_message'),
            font=('Helvetica', 12),
            wraplength=600
        )
        welcome_label.pack(pady=20, padx=20, fill=tk.X)
        
        # Recent projects frame
        recent_frame = ttk.LabelFrame(self.content, text=tr('recent_projects'))
        recent_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Placeholder for recent projects list
        self.recent_listbox = tk.Listbox(recent_frame)
        self.recent_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Load recent projects
        self.load_recent_projects()
    
    def load_recent_projects(self):
        """Load recent projects from settings."""
        # This would load from a settings file in a real app
        self.recent_listbox.delete(0, tk.END)
        self.recent_listbox.insert(tk.END, tr('no_recent_projects'))
    
    def new_project(self):
        """Create a new project."""
        dialog = NewProjectDialog(self.root, self._on_project_created)
        if dialog.show():
            self.status_var.set(tr('project_created'))
    
    def _on_project_created(self, project_path):
        """Handle project creation."""
        self.current_project = project_path
        self.project_path = project_path
        self.status_var.set(tr('project_loaded').format(project_path))
    
    def open_project(self):
        """Open an existing project."""
        project_path = filedialog.askdirectory(
            title=tr('select_project_directory'),
            mustexist=True
        )
        if project_path:
            self._on_project_created(project_path)
    
    def _create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        # Clear any existing widgets in the sidebar
        for widget in self.sidebar.winfo_children():
            widget.destroy()
        
        # Project section
        ttk.Label(
            self.sidebar,
            text=tr('project').upper(),
            style='Bold.TLabel'
        ).pack(fill=tk.X, padx=5, pady=(10, 5), anchor=tk.W)
        
        ttk.Button(
            self.sidebar,
            text=tr('new_project'),
            command=self.new_project,
            style='Accent.TButton'
        ).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(
            self.sidebar,
            text=tr('open_project'),
            command=self.open_project
        ).pack(fill=tk.X, padx=5, pady=2)
        
        # Package section
        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Label(
            self.sidebar,
            text=tr('package').upper(),
            style='Bold.TLabel'
        ).pack(fill=tk.X, padx=5, pady=(0, 5), anchor=tk.W)
        
        ttk.Button(
            self.sidebar,
            text=tr('install_package'),
            command=self.install_package
        ).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(
            self.sidebar,
            text=tr('uninstall_package'),
            command=self.uninstall_package
        ).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(
            self.sidebar,
            text=tr('update_package'),
            command=self.update_package
        ).pack(fill=tk.X, padx=5, pady=2)
        
        # Repository section
        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Label(
            self.sidebar,
            text=tr('repositories').upper(),
            style='Bold.TLabel'
        ).pack(fill=tk.X, padx=5, pady=(0, 5), anchor=tk.W)
        
        ttk.Button(
            self.sidebar,
            text=tr('manage_repositories'),
            command=self.manage_repositories
        ).pack(fill=tk.X, padx=5, pady=2)
        
        # Dependencies section
        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Label(
            self.sidebar,
            text=tr('dependencies').upper(),
            style='Bold.TLabel'
        ).pack(fill=tk.X, padx=5, pady=(0, 5), anchor=tk.W)
        
        ttk.Button(
            self.sidebar,
            text=tr('manage_dependencies'),
            command=self.manage_dependencies
        ).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(
            self.sidebar,
            text=tr('check_conflicts'),
            command=self.check_conflicts
        ).pack(fill=tk.X, padx=5, pady=2)
        
        # Help section
        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Button(
            self.sidebar,
            text=tr('help'),
            command=self.show_help
        ).pack(fill=tk.X, padx=5, pady=2)
        
        # Configure sidebar
        self.sidebar.pack_propagate(False)
    
    def install_package(self):
        """Install a package."""
        package = simpledialog.askstring(
            tr('install_package'),
            tr('enter_package_name')
        )
        if package:
            self.status_var.set(tr('installing_package').format(package))
            # Implementation would go here
    
    def uninstall_package(self):
        """Uninstall a package."""
        self.status_var.set(tr('uninstall_package_not_implemented'))
    
    def update_package(self):
        """Update a package."""
        self.status_var.set(tr('update_package_not_implemented'))
    
    def manage_repositories(self):
        """Open repository manager dialog."""
        from struttura.repository_ui import RepositoryManagerFrame
        
        # Create a top-level window for the repository manager
        repo_window = tk.Toplevel(self.root)
        repo_window.title(tr('manage_repositories'))
        
        # Set window size and position
        window_width = 700
        window_height = 500
        screen_width = repo_window.winfo_screenwidth()
        screen_height = repo_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        repo_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create the repository manager frame
        repo_frame = RepositoryManagerFrame(repo_window, self.repository_manager)
        repo_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Set focus to the new window
        repo_window.focus_set()
        repo_window.grab_set()
        
        # Update status
        self.status_var.set(tr('managing_repositories'))
    
    def manage_dependencies(self):
        """Open dependency manager dialog."""
        from struttura.dependency_ui import DependencyDialog
        
        if not self.project_path:
            messagebox.showerror(tr('error'), tr('no_project_open'))
            return
            
        try:
            # Create and show the dependency dialog
            dialog = DependencyDialog(
                self.root,
                project_path=self.project_path,
                on_install=self._on_dependencies_installed
            )
            # Wait for the dialog to close
            self.root.wait_window(dialog)
            self.status_var.set(tr('dependencies_managed'))
        except Exception as e:
            messagebox.showerror(tr('error'), f"{tr('error_managing_dependencies')}: {str(e)}")
            self.log(f"Error managing dependencies: {str(e)}")
    
    def _on_dependencies_installed(self):
        """Callback when dependencies are installed."""
        self.status_var.set(tr('dependencies_installed'))
        # Refresh package list or update UI as needed
        if hasattr(self, 'refresh_package_list'):
            self.refresh_package_list()
    
    def check_conflicts(self):
        """Check for dependency conflicts."""
        self.status_var.set(tr('check_conflicts_not_implemented'))
    
    def show_help(self):
        """Show help information."""
        messagebox.showinfo(
            tr('help'),
            tr('help_message')
        )
    
    def load_settings(self):
        """Load application settings from file."""
        config_dir = os.path.join(os.path.expanduser('~'), '.python_package_manager')
        config_file = os.path.join(config_dir, 'config.json')
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
                    
                # Apply settings
                if 'window_geometry' in self.settings:
                    self.root.geometry(self.settings['window_geometry'])
                    
                if 'last_project' in self.settings and self.settings['last_project']:
                    if os.path.exists(self.settings['last_project']):
                        self._on_project_created(self.settings['last_project'])
                        
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save application settings to file."""
        try:
            # Update current window geometry
            self.settings['window_geometry'] = self.root.geometry()
            
            # Save to file
            config_dir = os.path.join(os.path.expanduser('~'), '.python_package_manager')
            os.makedirs(config_dir, exist_ok=True)
            config_file = os.path.join(config_dir, 'config.json')
            
            with open(config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
                
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def check_gpg_installed(self):
        """Check if GPG is installed and available."""
        try:
            subprocess.run(
                ['gpg', '--version'],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            messagebox.showerror("Error", "GPG is not installed. Please install GPG to sign packages.")
            return False
            
    def sign_package(self):
        """Sign the package with GPG."""
        if not self.check_gpg_installed():
            messagebox.showerror(
                tr('gpg_not_found'),
                tr('gpg_not_found_message')
            )
            return False
            
        if not self.project_path:
            messagebox.showerror(
                tr('no_project'),
                tr('no_project_message')
            )
            return False
            
        # Build the package first
        if not self.build_package():
            return False
            
        # Find the built package
        dist_dir = os.path.join(self.project_path, 'dist')
        if not os.path.exists(dist_dir):
            messagebox.showerror(
                tr('build_error'),
                tr('build_directory_not_found')
            )
            return False
            
        # Find the latest package file
        try:
            package_files = [f for f in os.listdir(dist_dir) 
                          if f.endswith(('.tar.gz', '.whl'))]
            if not package_files:
                messagebox.showerror(
                    tr('no_package_found'),
                    tr('no_package_found_message')
                )
                return False
                
            package_file = os.path.join(dist_dir, max(package_files, 
                                                  key=lambda x: os.path.getmtime(os.path.join(dist_dir, x))))
            
            # Sign the package
            result = subprocess.run(
                ['gpg', '--detach-sign', '-a', package_file],
                cwd=dist_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                messagebox.showinfo(
                    tr('sign_success'),
                    tr('package_signed_successfully')
                )
                return True
            else:
                messagebox.showerror(
                    tr('sign_error'),
                    f"{tr('failed_to_sign_package')}:\n{result.stderr}"
                )
                return False
                
        except Exception as e:
            messagebox.showerror(
                tr('error'),
                f"{tr('error_signing_package')}: {str(e)}"
            )
            return False
        except (subprocess.SubprocessError, FileNotFoundError):
            messagebox.showerror("Error", "GPG is not installed. Please install GPG to sign packages.")
            return False
            
    def sign_package(self):
        """Sign the package with GPG."""
        if not self.check_gpg_installed():
            return
            
        # Build the package first
        self.log("\n=== Building package for signing ===")
        if not self.build_package():
            return
            
    def on_close(self):
        """Handle window close event."""
        if messagebox.askokcancel(tr('quit'), tr('quit_confirmation')):
            self.save_settings()
            self.root.destroy()
    
    def sign_package(self):
        """Sign the package with GPG."""
        if not self.check_gpg_installed():
            return False
            
        if not self.current_project:
            messagebox.showerror("Error", "No project is currently open.")
            return False
            
        # Build the package first
        self.log("\n=== Building package for signing ===")
        if not self.build_package():
            return False
            
        # Sign the package
        dist_dir = os.path.join(self.current_project, 'dist')
        if not os.path.exists(dist_dir):
            self.log("Error: dist directory not found")
            return False
            
        self.log("\n=== Signing package with GPG ===")
        try:
            # Find the latest built package
            dist_files = sorted(os.listdir(dist_dir))
            if not dist_files:
                self.log("Error: No package files found in dist directory")
                return False
                
            package_file = os.path.join(dist_dir, dist_files[-1])
            result = subprocess.run(
                ['gpg', '--detach-sign', '-a', package_file],
                capture_output=True,
                text=True,
                check=True
            )
            self.log(f"Successfully signed package: {package_file}.asc")
            return True
            
        except subprocess.CalledProcessError as e:
            self.log(f"Error signing package: {e.stderr}")
            return False
            
        except Exception as e:
            self.log(f"Error: {str(e)}")
            return False
            
    # Virtual Environment UI Handlers
    def browse_python(self):
        """Open file dialog to select Python interpreter."""
        python_path = filedialog.askopenfilename(
            title="Select Python Interpreter",
            filetypes=[("Python Executable", "python.exe;python3;python3.*")]
        )
        if python_path:
            self.python_path.delete(0, tk.END)
            self.python_path.insert(0, python_path)
            
    def browse_venv(self):
        """Open directory dialog to select virtual environment."""
        venv_dir = filedialog.askdirectory(title="Select Virtual Environment Directory")
        if venv_dir:
            self.venv_path.delete(0, tk.END)
            self.venv_path.insert(0, venv_dir)
            
    def on_create_venv(self):
        """Handle Create Virtual Environment button click."""
        venv_dir = self.venv_path.get().strip()
        python_exe = self.python_path.get().strip()
        
        if not venv_dir:
            messagebox.showerror("Error", "Please specify a directory for the virtual environment")
            return
            
        # If python_exe is not specified, use the current interpreter
        if not python_exe:
            python_exe = sys.executable
            
        self.create_virtualenv(venv_dir, python_exe if python_exe != sys.executable else None)
        
    def on_activate_venv(self):
        """Handle Activate Virtual Environment button click."""
        venv_dir = self.venv_path.get().strip()
        if not venv_dir:
            messagebox.showerror("Error", "Please specify a virtual environment directory")
            return
            
        if not os.path.exists(os.path.join(venv_dir, 'pyvenv.cfg')):
            if not messagebox.askyesno("Confirm", 
                                     "This directory doesn't appear to be a virtual environment.\n"
                                     "Do you want to create a new virtual environment here?"):
                return
            self.create_virtualenv(venv_dir, self.python_path.get().strip() or None)
            
        self.activate_virtualenv(venv_dir)
        
    def on_deactivate_venv(self):
        """Handle Deactivate Virtual Environment button click."""
        if hasattr(self, 'original_env'):
            self.deactivate_virtualenv()
        else:
            self.log("No active virtual environment to deactivate")
            
    def on_install_to_venv(self):
        """Handle Install Package button click."""
        if 'VIRTUAL_ENV' not in os.environ:
            messagebox.showerror("Error", "Please activate a virtual environment first")
            return
            
        package = simpledialog.askstring("Install Package", "Enter package name or path to install:")
        if package:
            self.install_to_virtualenv(package)
    
    def run_command(self, command, cwd=None):
        self.log(f"$ {' '.join(command)}")
        try:
            result = subprocess.run(
                command,
                cwd=cwd or os.getcwd(),
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout:
                self.log(result.stdout)
            if result.stderr:
                self.log(f"Error: {result.stderr}")
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            self.log(f"Command failed with error: {e.stderr}")
            return False
    
    def initialize_package(self):
        path = self.project_path.get()
        if not path:
            messagebox.showerror(tr("error"), tr("select_project_directory"))
            return
        
        package_name = self.package_name.get()
        if not package_name:
            messagebox.showerror(tr("error"), tr("enter_package_name"))
            return
        
        # Create basic package structure
        os.makedirs(os.path.join(path, package_name), exist_ok=True)
        with open(os.path.join(path, package_name, '__init__.py'), 'w') as f:
            f.write(f'"""{package_name} package"""\n')
        
        # Create setup.py
        setup_content = f"""from setuptools import setup, find_packages

setup(
    name="{package_name}",
    version="{self.version.get()}",
    packages=find_packages(),
    install_requires=[],
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/{package_name}",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)"""
        
        with open(os.path.join(path, 'setup.py'), 'w') as f:
            f.write(setup_content)
        
        # Create README.md
        with open(os.path.join(path, 'README.md'), 'w') as f:
            f.write(f"# {package_name}\n\nA Python package.")
        
        self.log(f"Package {package_name} initialized at {path}")
    
    def build_package(self):
        if not self.project_path:
            messagebox.showerror("Error", "Please select a project directory")
            return False
            
        self.log("Building package...")
        if self.run_command([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'], cwd=self.project_path):
            self.log("Package built successfully!")
            return True
        return False
    
    def install_package(self):
        if not self.project_path:
            messagebox.showerror("Error", "Please select a project directory")
            return False
            
        self.log("Installing package in development mode...")
        if self.run_command([sys.executable, '-m', 'pip', 'install', '-e', '.'], cwd=self.project_path):
            self.log("Package installed in development mode!")
            return True
        return False
    
    def upload_to_pypi(self):
        path = self.project_path.get()
        if not path:
            messagebox.showerror("Error", "Please select a project directory")
            return
        
        self.log("Uploading to PyPI...")
        if self.run_command([sys.executable, '-m', 'twine', 'upload', 'dist/*'], cwd=path):
            self.log("Package uploaded to PyPI successfully!")

def main():
    root = tk.Tk()
    try:
        app = PyPackagerApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
