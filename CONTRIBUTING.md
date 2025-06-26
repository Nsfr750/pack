<!-- markdownlint-disable MD051 -->
# Contributing to Python Package Manager
<!-- markdownlint-enable MD051 -->

First off, thank you for considering contributing to Python Package Manager! We appreciate your interest in making Python packaging easier for everyone.

## 📜 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report any unacceptable behavior to the project maintainers.

## 🤝 How Can I Contribute?

### 🐛 Reporting Bugs

1. **Check existing issues** to ensure the bug hasn't been reported yet.
2. **Create a new issue** with the following details:
   - Clear, descriptive title
   - Detailed description of the issue
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots or screen recordings if applicable
   - Any relevant error messages or logs

### 💡 Suggesting Enhancements

1. Check if a similar feature request exists
2. Open a new issue with:
   - Clear description of the enhancement
   - Use case and benefits
   - Any relevant examples or references
   - Screenshots/mockups if applicable

### 💻 Code Contributions

#### Setting Up for Development

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:

   <!-- markdownlint-disable MD031 -->
   ```bash
   git clone https://github.com/your-username/pack.git
   cd pack
   ```
   <!-- markdownlint-enable MD031 -->

3. **Set up development environment** (see [Development Setup](#-development-setup) section below)

4. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Make your changes** following the [coding standards](#-coding-standards)

6. **Run tests** and ensure they pass:

   ```bash
   pytest
   ```

7. **Commit your changes** with a descriptive message:

   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

8. **Push** to your fork and open a pull request

### 🔍 Code Review Process

1. Ensure all CI checks pass
2. A maintainer will review your PR
3. Address any feedback or requested changes
4. Once approved, your changes will be merged

## 🛠 Development Setup

### Prerequisites

- Python 3.8+
- Git
- pip (latest version)
- Virtual environment (recommended)

### Local Development

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Nsfr750/pack.git
   cd pack
   ```

2. **Set up virtual environment**:

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Unix/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -e ".[dev]"
   ```

4. **Set up pre-commit hooks**:

   ```bash
   pre-commit install
   ```

### 🧪 Testing

Run the test suite with:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pack tests/

# Run a specific test file
pytest tests/test_module.py

# Run a specific test
pytest tests/test_module.py::test_function

# Generate HTML coverage report
coverage html
```

### 📚 Documentation

Documentation is built with Sphinx. To build locally:

```bash
cd docs
make html
```

The documentation will be available in `docs/_build/html/index.html`.

## 🧹 Code Quality

We use several tools to maintain code quality:

| Tool | Purpose | Command |
|------|---------|---------|
| [Black](https://black.readthedocs.io/) | Code formatting | `black .` |
| [isort](https://pycqa.github.io/isort/) | Import sorting | `isort .` |
| [Flake8](https://flake8.pycqa.org/) | Linting | `flake8` |
| [Mypy](https://mypy.readthedocs.io/) | Static type checking | `mypy .` |

Run all code style checks:

```bash
pre-commit run --all-files
```

## 📝 Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all new code
- Write docstrings following [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Keep functions small and focused
- Write tests for new functionality
- Update documentation when adding new features

### Git Commit Messages

- Use the [Conventional Commits](https://www.conventionalcommits.org/) format
- Start with a type: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`
- Keep the first line under 50 characters
- Include a detailed description when necessary
- Reference issues and pull requests when applicable

## 🔄 Pull Request Process

1. **Branch Naming**:
   - `feature/` - New features
   - `bugfix/` - Bug fixes
   - `docs/` - Documentation changes
   - `refactor/` - Code refactoring
   - `test/` - Test-related changes

2. **Pull Request Checklist**:
   - [ ] Tests pass
   - [ ] Documentation updated (if needed)
   - [ ] Code follows style guidelines
   - [ ] Changes are well-documented
   - [ ] Changes are backward compatible
   - [ ] All new and existing tests pass

3. **Review Process**:
   - At least one approval required before merging
   - All CI checks must pass
   - Maintainers will review your PR and may request changes

## 🌐 Community

- **Discord**: [Join our community](https://discord.gg/your-invite-link)
- **Twitter**: [@Nsfr750](https://twitter.com/Nsfr750)
- **Email**: [nsfr750@yandex.com](mailto:nsfr750@yandex.com)

## 🏷 Versioning

We follow [Semantic Versioning](https://semver.org/). For the versions available, see the [tags on this repository](https://github.com/Nsfr750/pack/tags).

## 📄 License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve this project!
- Special thanks to our sponsors and supporters.

## Project Structure

```text
pack/
├── struttura/         # Core application modules
├── gui/               # GUI components
├── images/            # Prj PNG/ICO
├── tests/             # Test suite
├── docs/              # Documentation
└── scripts/           # Utility scripts
```

## Questions?

Feel free to [open an issue](https://github.com/Nsfr750/pack/issues) or contact us at [nsfr750@yandex.com](mailto:nsfr750@yandex.com)
