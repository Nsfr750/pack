# Python Package Manager GUI

![Python Package Manager](images/ita.png)
![Python Package Manager](images/eng.png)

A modern, user-friendly GUI application built with CustomTkinter for managing Python packages. Streamline your Python package development workflow with an intuitive interface.

[![GitHub release](https://img.shields.io/badge/release-v1.1.0-green.svg?style=for-the-badge)](https://github.com/Nsfr750/pack/releases/tag/v1.1.0)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/gpl-3.0)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/Nsfr750/pack/graphs/commit-activity)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

## ✨ Features

### Package Management

- 🏗️ Initialize new Python packages with customizable templates
- 🔧 Build source distribution and wheel packages with a single click
- ⚡ Install packages in development mode with automatic dependency handling
- ☁️ Upload packages to PyPI with secure credential management
- 🔍 Search and manage installed packages

### Development Tools

- 📝 Built-in Markdown viewer for documentation
- 📊 Real-time logging and console output
- 🧪 Automated testing integration
- ✅ Code quality checks with flake8 and mypy

### User Experience

- 🌍 Multi-language support (English/Italian)
- 🎨 Modern, customizable UI with light/dark theme support
- ⌨️ Keyboard shortcuts for power users
- 🔄 Automatic update checking

## 🚀 Requirements

- Python 3.8 or higher
- pip (latest version recommended)
- Git (for version control integration)

## 📦 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Nsfr750/pack.git
   cd pack
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Usage

### Running the Application

```bash
python main.py
```

### Basic Workflow

1. **Project Setup**
   - Select your project directory
   - Use "Initialize Package" for new projects
   - Configure package metadata through the intuitive UI

2. **Development**
   - Edit your package code in your preferred editor
   - Use the built-in tools to manage dependencies
   - Check for updates to dependencies

3. **Building & Distribution**
   - Build source and wheel distributions
   - Validate package metadata
   - Install in development mode with a single click
   - Upload to PyPI when ready

## 🛠️ Development

### Project Structure

```text
pack/
├── struttura/         # Core application modules
├── gui/               # GUI components
├── tests/             # Test suite
├── main.py            # Application entry point
└── requirements.txt   # Project dependencies
```

### Running Tests

```bash
pytest tests/
```

### Code Style

This project uses:

- Black for code formatting
- Flake8 for linting
- Type hints throughout the codebase

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ using Python and CustomTkinter
- Inspired by the needs of Python package maintainers
- Thanks to all contributors who have helped improve this project
