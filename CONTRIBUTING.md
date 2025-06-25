# Contributing to Python Package Manager

First off, thank you for considering contributing to Python Package Manager! It's people like you that make Python Package Manager such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

1. **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/Nsfr750/pack/issues).
2. If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/Nsfr750/pack/issues/new). Be sure to include:
   - A clear, descriptive title
   - A detailed description of the issue
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Screenshots if applicable

### Submitting Changes

1. **Fork** the repository on GitHub
2. **Clone** your fork locally

   ```bash
   git clone https://github.com/your-username/pack.git
   cd pack
   ```

3. **Create a branch** for your changes

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. Make your changes
5. Run tests and ensure they pass

   ```bash
   pytest
   ```

6. **Commit** your changes

   ```bash
   git add .
   git commit -m "Add your feature description"
   ```

7. **Push** to your fork and submit a pull request

   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (latest version recommended)
- Git
- (Optional) Virtual environment (venv, conda, etc.)

### Local Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Nsfr750/pack.git
   cd pack
   ```

2. **Create and activate a virtual environment**:

   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On Unix or MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install development dependencies**:

   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

4. **Install pre-commit hooks**:

   ```bash
   pre-commit install
   ```

### Using GitHub Codespaces (Recommended)

1. Click the "Code" button on the repository page
2. Select "Open with Codespaces"
3. Create a new codespace
4. The environment will be set up automatically

## Code Style

We enforce consistent code style using the following tools:

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

## Testing

### Running Tests

We use `pytest` for testing. To run the test suite:

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_module.py

# Run a specific test
pytest tests/test_module.py::test_function
```

### Test Coverage

To generate a coverage report:

```bash
pytest --cov=pack --cov-report=term-missing
```

### Linting

Run the linter:

```bash
flake8
```

## Documentation

We use Sphinx for documentation. To build the documentation locally:

```bash
cd docs
make html
```

The documentation will be available in `docs/_build/html/index.html`.

## Pull Request Process

1. **Branch Naming**:
   - `feature/` - New features
   - `bugfix/` - Bug fixes
   - `docs/` - Documentation changes
   - `refactor/` - Code refactoring
   - `test/` - Test-related changes

2. **Commit Messages**:
   - Use the present tense ("Add feature" not "Added feature")
   - Use the imperative mood ("Move button to..." not "Moves button to...")
   - Keep the first line under 50 characters
   - Reference issues and pull requests liberally

3. **Pull Request Checklist**:
   - [ ] Tests pass
   - [ ] Documentation updated (if needed)
   - [ ] Code follows style guidelines
   - [ ] Changes are well-documented
   - [ ] Changes are backward compatible
   - [ ] All new and existing tests pass

4. **Review Process**:
   - At least one approval required before merging
   - All CI checks must pass
   - Maintainers will review your PR and may request changes

## Reporting Issues

Before reporting an issue, please check if it has already been reported in the [GitHub Issues](https://github.com/Nsfr750/pack/issues).

When creating an issue report, please include:

1. **Description**: Clear and concise description of the bug
2. **Steps to Reproduce**:

   ```text
   1. Go to '...'
   2. Click on '....'
   3. Scroll down to '....'
   4. See error
   ```

3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Screenshots**: If applicable, add screenshots to help explain
6. **Environment**:
   - OS: [e.g., Windows 10, macOS Big Sur, Ubuntu 20.04]
   - Python Version: [e.g., 3.8.5]
   - Package Version: [e.g., 1.0.0]

## Feature Requests

We welcome feature requests! Before submitting a new feature request, please:

1. Check if a similar feature already exists or has been requested
2. Clearly describe the problem you're trying to solve
3. Explain why this feature would be valuable to other users
4. Provide any relevant use cases or examples

## Community

- **Discord**: [Join our community](https://discord.gg/your-invite-link)
- **Twitter**: [@Nsfr750](https://twitter.com/Nsfr750)
- **Email**: [nsfr750@yandex.com](mailto:nsfr750@yandex.com)

## License

By contributing, you agree that your contributions will be licensed under the [GPLv3 License](LICENSE).

## Project Structure

```text
pack/
├── struttura/         # Core application modules
├── gui/               # GUI components
├── tests/             # Test suite
├── docs/              # Documentation
└── scripts/           # Utility scripts
```

## Versioning

We use [Semantic Versioning](https://semver.org/). For the versions available, see the [tags on this repository](https://github.com/Nsfr750/pack/tags).

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

## Questions?

Feel free to [open an issue](https://github.com/Nsfr750/pack/issues) or contact us at [nsfr750@yandex.com](mailto:nsfr750@yandex.com)
