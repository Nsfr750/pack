import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import sys
import json
from pathlib import Path
from struttura.menu import create_menu_bar
from struttura.lang import tr

class PyPackagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(tr("app_title"))
        self.root.geometry("800x600")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', padding=5)
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=5)
        
        # Create menu
        self.menubar = create_menu_bar(self.root, self)
        self.root.config(menu=self.menubar)
        
        self.create_widgets()
        self.current_project = None
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Project info frame
        project_frame = ttk.LabelFrame(main_frame, text=tr("project_info"), padding=10)
        project_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Project path
        ttk.Label(project_frame, text=tr("project_path") + ":").grid(row=0, column=0, sticky=tk.W)
        self.project_path = tk.StringVar()
        ttk.Entry(project_frame, textvariable=self.project_path, width=50).grid(row=0, column=1, padx=5, sticky=tk.EW)
        ttk.Button(project_frame, text=tr("browse"), command=self.browse_project).grid(row=0, column=2, padx=5)
        
        # Package info
        ttk.Label(project_frame, text=tr("package_name") + ":").grid(row=1, column=0, sticky=tk.W)
        self.package_name = tk.StringVar()
        ttk.Entry(project_frame, textvariable=self.package_name).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(project_frame, text=tr("version") + ":").grid(row=2, column=0, sticky=tk.W)
        self.version = tk.StringVar(value="0.1.0")
        ttk.Entry(project_frame, textvariable=self.version).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Actions frame
        actions_frame = ttk.LabelFrame(main_frame, text=tr("package_actions"), padding=10)
        actions_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(actions_frame, text=tr("initialize_package"), command=self.initialize_package).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text=tr("build_package"), command=self.build_package).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text=tr("install_package"), command=self.install_package).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text=tr("upload_to_pypi"), command=self.upload_to_pypi).pack(side=tk.LEFT, padx=5)
        
        # Console output
        console_frame = ttk.LabelFrame(main_frame, text=tr("output"), padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        self.console = tk.Text(console_frame, wrap=tk.WORD, bg='black', fg='white')
        scrollbar = ttk.Scrollbar(console_frame, orient="vertical", command=self.console.yview)
        self.console.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console.pack(fill=tk.BOTH, expand=True)
    
    def browse_project(self):
        path = filedialog.askdirectory()
        if path:
            self.project_path.set(path)
            self.load_project_info(path)
    
    def load_project_info(self, path):
        self.current_project = path
        # Try to load package info if setup.py exists
        setup_py = os.path.join(path, 'setup.py')
        if os.path.exists(setup_py):
            try:
                with open(setup_py, 'r') as f:
                    content = f.read()
                    # Simple extraction of package name and version (for demo)
                    import re
                    name_match = re.search(r'name=[\'"]([^\"]+)[\'"]', content)
                    version_match = re.search(r'version=[\'"]([^\"]+)[\'"]', content)
                    
                    if name_match:
                        self.package_name.set(name_match.group(1))
                    if version_match:
                        self.version.set(version_match.group(1))
            except Exception as e:
                self.log(f"Error reading setup.py: {str(e)}")
            except Exception as e:
                self.log(f"Error reading setup.py: {str(e)}")
    
    def log(self, message):
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.root.update_idletasks()
    
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
        path = self.project_path.get()
        if not path:
            messagebox.showerror("Error", "Please select a project directory")
            return
        
        self.log("Building package...")
        if self.run_command([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'], cwd=path):
            self.log("Package built successfully!")
    
    def install_package(self):
        path = self.project_path.get()
        if not path:
            messagebox.showerror("Error", "Please select a project directory")
            return
        
        self.log("Installing package in development mode...")
        if self.run_command([sys.executable, '-m', 'pip', 'install', '-e', '.'], cwd=path):
            self.log("Package installed in development mode!")
    
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
