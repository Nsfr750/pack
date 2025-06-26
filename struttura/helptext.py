"""
Help text for Python Package Manager

This module contains the help documentation that was originally in HELP.md.
"""

HELP_TEXT = """# Python Package Manager - Help Guide

[![Documentation Status](https://readthedocs.org/projects/python-package-manager/badge/?version=latest)](https://python-package-manager.readthedocs.io/)
[![GitHub Issues](https://img.shields.io/github/issues/Nsfr750/pack)](https://github.com/Nsfr750/pack/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Nsfr750/pack)](https://github.com/Nsfr750/pack/pulls)

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Features](#features)
4. [Advanced Usage](#advanced-usage)
5. [Troubleshooting](#troubleshooting)
6. [FAQ](#faq)
7. [Contributing](#contributing)
8. [Need Help?](#need-help)

## Getting Started

### System Requirements

- Python 3.8 or higher
- pip (latest version recommended)
- Git (for version control integration)
- Tcl/Tk (usually included with Python on Windows/macOS)

### Installation

#### From PyPI (Recommended)

```bash
pip install python-package-manager
```

#### From Source

1. Clone the repository:

   ```bash
   git clone https://github.com/Nsfr750/pack.git
   cd pack
   ```

2. Install the package in development mode:

   ```bash
   pip install -e .
   ```

### First Run

After installation, you can start the application by running:

```bash
python -m pack
```

## Basic Usage

### Creating a New Package

1. Click on "File" > "New Project"
2. Select a directory for your project
3. Enter your package details (name, version, etc.)
4. Click "Create" to initialize the package structure

### Building a Package

1. Open your project
2. Click on the "Build Package" button
3. The built packages will be placed in the `dist` directory

### Installing a Package

1. Open your project
2. Click on the "Install Package" button
3. The package will be installed in development mode

## Features

### Package Management

- Initialize new Python packages
- Build source distribution and wheel packages
- Install packages in development mode
- Upload packages to PyPI

### Development Tools

- Built-in Markdown viewer for documentation
- Real-time logging and console output
- Automated testing integration
- Code quality checks

### User Experience

- Multi-language support
- Modern, customizable UI
- Keyboard shortcuts
- Automatic update checking

## Advanced Usage

### Configuration

You can configure the application by creating a `config.json` file in the application's configuration directory:

- **Windows**: `%APPDATA%\Python Package Manager\config.json`
- **macOS**: `~/Library/Application Support/Python Package Manager/config.json`
- **Linux**: `~/.config/python-package-manager/config.json`

Example configuration:

```json
{
    "theme": "system",
    "language": "en",
    "check_for_updates": true,
    "python_path": "python"
}
```

### Command Line Interface

The application also provides a command line interface:

```bash
# Start the GUI
python -m pack

# Initialize a new package
python -m pack init my_package

# Build a package
python -m pack build

# Install a package in development mode
python -m pack install
```

## Troubleshooting

### Common Issues

#### Missing Dependencies

If you encounter missing dependencies, try:

```bash
pip install -r requirements.txt
```

#### GUI Not Starting

Make sure you have Tkinter installed:

- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: Should be included with Python from python.org

#### Package Installation Fails

- Check your internet connection
- Make sure you have write permissions to the installation directory
- Try running the application as administrator/root

## FAQ

### How do I update the application?

The application will automatically check for updates on startup. You can also manually check for updates in the "Help" menu or check the GitHub releases page.

### Can I use this with virtual environments?

Yes! The application works with virtual environments. Make sure to activate your virtual environment before running the application.

### Can I use this with existing projects?

Yes! Just open your project directory and the application will detect your package structure.

### How do I change the language?

Go to "Settings" > "Language" (or "Language" in the menu bar) and select your preferred language from the dropdown menu.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more information on how to get started.

### Development Setup

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=pack tests/
```

## Troubleshooting

### Common Issues

#### Package Not Found

- Ensure you've activated your virtual environment
- Check your PYTHONPATH
- Verify package installation with `pip list`

### Build Failures

- Check for syntax errors in your code
- Verify `setup.py` or `pyproject.toml` is correctly configured
- Check for missing dependencies

### PyPI Upload Issues

- Verify your PyPI credentials
- Check if the package name is available
- Ensure you're using the correct repository URL

## Need Help?

- Check the [GitHub Issues](https://github.com/Nsfr750/pack/issues)
- Join our [Discord Server](https://discord.gg/BvvkUEP9)
- Email: [nsfr750@yandex.com](mailto:nsfr750@yandex.com)

---

📝 *Documentation last updated: June 2025*
"""
