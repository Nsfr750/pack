# Python Package Manager - Help Guide

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
   
   Or install with all development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### First Run

1. Launch the application:
   ```bash
   python -m pack
   ```

2. The main window will open with the following components:
   - **Menu Bar**: Access all application features
   - **Project Panel**: View and manage your project files
   - **Console**: See command output and logs
   - **Status Bar**: Check the current status and language

## Basic Usage

### Creating a New Project

1. Click on `File` > `New Project`
2. Select a directory for your project
3. Enter your package details:
   - Package name
   - Version
   - Author
   - Description
   - License
4. Click `Create` to initialize the project structure

### Building Packages

1. Open your project
2. Click on `Build` in the toolbar or select `Build` from the menu
3. The built packages will be available in the `dist` directory

### Installing in Development Mode

1. Open your project
2. Click on `Install` in the toolbar or select `Install` from the menu
3. The package will be installed in development mode

## Features

### Package Management

- Initialize new Python packages
- Build source distributions and wheels
- Install packages in development mode
- Upload packages to PyPI
- Manage package dependencies

### Development Tools

- Integrated terminal for command-line access
- Tabbed help system with comprehensive documentation
- Real-time logging and console output
- Syntax highlighting for Python files
- Code formatting with Black
- Linting with flake8
- Type checking with mypy

### User Interface

- Modern, customizable UI with light/dark themes
- Multi-language support (English/Italian)
- Keyboard shortcuts for common actions
- Tabbed interface for better organization
- Status bar with useful information

## Advanced Usage

### Customizing the Build Process

You can customize the build process by editing the `pyproject.toml` or `setup.py` file in your project directory.

### Using the Integrated Terminal

The integrated terminal allows you to run shell commands without leaving the application. You can access it from the `Tools` > `Terminal` menu.

### Keyboard Shortcuts

- `Ctrl+N`: New Project
- `Ctrl+O`: Open Project
- `Ctrl+S`: Save
- `Ctrl+Shift+S`: Save As
- `F1`: Show Help
- `F5`: Run Project
- `Ctrl+Q`: Quit

## Troubleshooting

### Common Issues

#### Package Installation Fails
- Check your internet connection
- Make sure you have the required build tools installed
- Check the console for detailed error messages

#### Build Fails
- Check for syntax errors in your code
- Verify `setup.py` or `pyproject.toml` is correctly configured
- Check for missing dependencies

#### UI Issues
- Try resetting the UI settings from the `View` menu
- Check the console for any error messages
- If the issue persists, delete the configuration file and restart the application

## FAQ

### How do I change the language?
Go to `View` > `Language` and select your preferred language.

### How do I report a bug?
Please open an issue on our [GitHub repository](https://github.com/Nsfr750/pack/issues) with a detailed description of the problem.

### How can I contribute?
We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more information.

## Need Help?

If you need further assistance, please:

1. Check the [documentation](https://python-package-manager.readthedocs.io/)
2. Search the [GitHub issues](https://github.com/Nsfr750/pack/issues)
3. Open a new issue if your problem isn't already reported

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

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
