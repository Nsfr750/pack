"""
Package templates for different types of Python projects.
"""
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import shutil
import json

class PackageTemplate:
    """Base class for package templates."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def create(self, path: str, package_name: str, **kwargs) -> bool:
        """Create the template in the specified path."""
        raise NotImplementedError("Subclasses must implement create()")


class BasicPackageTemplate(PackageTemplate):
    """Basic Python package template."""
    
    def __init__(self):
        super().__init__(
            name="basic",
            description="A basic Python package with minimal structure"
        )
    
    def create(self, path: str, package_name: str, **kwargs) -> bool:
        """Create a basic Python package."""
        try:
            # Create package directory
            package_dir = Path(path) / package_name
            package_dir.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py
            (package_dir / "__init__.py").write_text(
                f'"""{package_name} package."""\n'
                f'__version__ = "0.1.0"\n'
            )
            
            # Create setup.py
            setup_content = f"""from setuptools import setup, find_packages

setup(
    name="{package_name}",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/{package_name}",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
"""
            (Path(path) / "setup.py").write_text(setup_content)
            
            # Create README.md
            readme_content = f"""# {package_name}

A Python package.

## Installation

```bash
pip install -e .
```

## Usage

```python
import {package_name}
```
"""
            (Path(path) / "README.md").write_text(readme_content)
            
            # Create requirements.txt
            (Path(path) / "requirements.txt").write_text("")
            
            # Create tests directory
            tests_dir = Path(path) / "tests"
            tests_dir.mkdir()
            (tests_dir / "__init__.py").write_text("")
            (tests_dir / "test_basic.py").write_text(
                f'"""Tests for {package_name}."""\n'
                'def test_import():\n'
                '    """Test that the package can be imported."""\n'
                f'    import {package_name}\n'
                f'    assert {package_name}.__version__ == "0.1.0"\n'
            )
            
            return True
            
        except Exception as e:
            print(f"Error creating basic package: {e}")
            return False


class CliPackageTemplate(PackageTemplate):
    """Command-line application package template."""
    
    def __init__(self):
        super().__init__(
            name="cli",
            description="A command-line application package with Click"
        )
    
    def create(self, path: str, package_name: str, **kwargs) -> bool:
        """Create a CLI application package."""
        try:
            # Create basic package structure
            basic = BasicPackageTemplate()
            if not basic.create(path, package_name, **kwargs):
                return False
                
            package_dir = Path(path) / package_name
            
            # Create main CLI module
            cli_content = '''import click

@click.group()
def cli():
    \"\"\"{package_name} - A command-line interface.\"\"\"
    pass

@cli.command()
@click.option('--name', default='World', help='Name to greet')
def hello(name):
    \"\"\"Say hello.\"\"\"
    click.echo(f'Hello, {{name}}!')

if __name__ == '__main__':
    cli()
'''
            (package_dir / "cli.py").write_text(cli_content.format(package_name=package_name))
            
            # Update __init__.py to expose the CLI
            with open(package_dir / "__init__.py", 'a') as f:
                f.write(f'\nfrom .cli import cli\n')
            
            # Update setup.py to include console_scripts
            setup_path = Path(path) / "setup.py"
            setup_content = setup_path.read_text()
            setup_content = setup_content.replace(
                'install_requires=[],',
                'install_requires=["click>=7.0"],\n    entry_points={\n        "console_scripts": [\n            f"{package_name}={package_name}.cli:cli",\n        ],\n    },'
            )
            setup_path.write_text(setup_content)
            
            # Update README.md with CLI instructions
            readme_path = Path(path) / "README.md"
            readme_content = readme_path.read_text()
            readme_content += """

## Command-line Usage

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run the CLI
{package_name} --help
{package_name} hello --name YourName
```
"""
            readme_path.write_text(readme_content)
            
            return True
            
        except Exception as e:
            print(f"Error creating CLI package: {e}")
            return False


class WebAppPackageTemplate(PackageTemplate):
    """Web application package template using Flask."""
    
    def __init__(self):
        super().__init__(
            name="web",
            description="A web application package with Flask"
        )
    
    def create(self, path: str, package_name: str, **kwargs) -> bool:
        """Create a web application package."""
        try:
            # Create basic package structure
            basic = BasicPackageTemplate()
            if not basic.create(path, package_name, **kwargs):
                return False
                
            package_dir = Path(path) / package_name
            
            # Create web application files
            (package_dir / "app.py").write_text("""from flask import Flask

def create_app():
    \"\"\"Create and configure the Flask application.\"\"\"
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return 'Hello, World!'
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
""")
            
            # Create templates directory
            templates_dir = package_dir / "templates"
            templates_dir.mkdir()
            (templates_dir / "base.html").write_text("""<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
""")
            
            (templates_dir / "index.html").write_text("""{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
<h1>Welcome to {{ app_name }}!</h1>
{% endblock %}
""")
            
            # Update setup.py
            setup_path = Path(path) / "setup.py"
            setup_content = setup_path.read_text()
            setup_content = setup_content.replace(
                'install_requires=[],',
                'install_requires=["flask>=2.0.0"],'
            )
            setup_path.write_text(setup_content)
            
            # Update README.md
            readme_path = Path(path) / "README.md"
            readme_content = readme_path.read_text()
            readme_content += """
## Web Application

### Development

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run the development server
export FLASK_APP={package_name}.app:create_app
export FLASK_ENV=development
flask run
```

Visit http://localhost:5000 in your browser.
"""
            readme_path.write_text(readme_content)
            
            return True
            
        except Exception as e:
            print(f"Error creating web app package: {e}")
            return False


class DataSciencePackageTemplate(PackageTemplate):
    """Data science project package template."""
    
    def __init__(self):
        super().__init__(
            name="data-science",
            description="A data science project with Jupyter, pandas, and scikit-learn"
        )
    
    def create(self, path: str, package_name: str, **kwargs) -> bool:
        """Create a data science project package."""
        try:
            # Create basic package structure
            basic = BasicPackageTemplate()
            if not basic.create(path, package_name, **kwargs):
                return False
                
            package_dir = Path(path) / package_name
            
            # Create data directory
            data_dir = Path(path) / "data"
            data_dir.mkdir()
            (data_dir / "raw").mkdir()
            (data_dir / "processed").mkdir()
            (data_dir / "external").mkdir()
            
            # Create notebooks directory
            notebooks_dir = Path(path) / "notebooks"
            notebooks_dir.mkdir()
            
            # Create example notebook
            (notebooks_dir / "01_exploratory.ipynb").write_text("""{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Exploratory Data Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# Load data\n",
    "# df = pd.read_csv('../data/raw/your_data.csv')\n",
    "\n",
    "# Explore data\n",
    "# df.head()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}""")
            
            # Create src directory for modules
            src_dir = Path(path) / "src"
            src_dir.mkdir()
            (src_dir / "__init__.py").write_text("")
            (src_dir / "data").mkdir()
            (src_dir / "features").mkdir()
            (src_dir / "models").mkdir()
            (src_dir / "visualization").mkdir()
            
            # Create requirements file
            (Path(path) / "requirements.txt").write_text("""# Core
numpy>=1.19.0
pandas>=1.0.0
matplotlib>=3.0.0
seaborn>=0.10.0
scikit-learn>=0.24.0
jupyter>=1.0.0
ipykernel

# Development
pytest>=6.0.0
black>=21.0
flake8>=3.8.0
""")
            
            # Update setup.py
            setup_path = Path(path) / "setup.py"
            setup_content = setup_path.read_text()
            setup_content = setup_content.replace(
                'packages=find_packages(),',
                'packages=find_packages() + ["src"],\n    package_dir={"": "."},'
            )
            setup_path.write_text(setup_content)
            
            # Update README.md
            readme_path = Path(path) / "README.md"
            readme_content = readme_path.read_text()
            readme_content += """
## Data Science Project

### Project Structure

```
.
data/               # Data files
    raw/            # Raw data
    processed/      # Processed data
    external/       # External data sources
notebooks/          # Jupyter notebooks
src/                # Source code
    data/           # Data processing
    features/       # Feature engineering
    models/         # Model code
    visualization/  # Visualization code
tests/              # Tests
.gitignore
README.md
requirements.txt
setup.py
```

### Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```
"""
            readme_path.write_text(readme_content)
            
            # Create .gitignore
            (Path(path) / ".gitignore").write_text("""# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# venv
venv/
env/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Data files
*.csv
*.h5
*.hdf5
*.pkl
*.pkl.gz
*.parquet

# Logs
logs/
*.log
""")
            
            return True
            
        except Exception as e:
            print(f"Error creating data science package: {e}")
            return False


class PackageTemplateManager:
    """Manages available package templates."""
    
    def __init__(self):
        self.templates: Dict[str, PackageTemplate] = {}
        self._register_default_templates()
    
    def _register_default_templates(self):
        """Register the default package templates."""
        self.register(BasicPackageTemplate())
        self.register(CliPackageTemplate())
        self.register(WebAppPackageTemplate())
        self.register(DataSciencePackageTemplate())
    
    def register(self, template: PackageTemplate):
        """Register a new package template."""
        self.templates[template.name] = template
    
    def get_template(self, name: str) -> Optional[PackageTemplate]:
        """Get a template by name."""
        return self.templates.get(name)
    
    def list_templates(self) -> List[Dict[str, str]]:
        """List all available templates."""
        return [
            {"name": name, "description": template.description}
            for name, template in self.templates.items()
        ]
    
    def create_from_template(
        self, 
        template_name: str, 
        path: str, 
        package_name: str, 
        **kwargs
    ) -> bool:
        """Create a new package from a template."""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Unknown template: {template_name}")
            
        path = os.path.abspath(path)
        package_dir = os.path.join(path, package_name)
        
        # Create the directory if it doesn't exist
        os.makedirs(package_dir, exist_ok=True)
        
        # Create the package using the template
        return template.create(path, package_name, **kwargs)


# Create a global instance of the template manager
template_manager = PackageTemplateManager()

def get_template_manager() -> PackageTemplateManager:
    """Get the global template manager instance."""
    return template_manager
