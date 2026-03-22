# Contributing to Parma

Thank you for your interest in contributing to Parma! This document provides guidelines for contributing to the project.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/lotherk/parma.git
   cd parma
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Run tests:
   ```bash
   python -m pytest
   ```

4. Run linting:
   ```bash
   python -m ruff check .
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for new code
- Write docstrings for public functions
- Keep lines under 88 characters

## Testing

- Add tests for new features in the `tests/` directory
- Ensure all tests pass before submitting a PR
- Include both unit tests and integration tests

## Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and add tests
4. Run the full test suite: `python -m pytest`
5. Commit your changes: `git commit -m "Add feature: your feature description"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

## Reporting Issues

- Use the issue templates provided
- Include detailed steps to reproduce
- Provide sample code when possible
- Specify your environment (Python version, OS, etc.)

## Code of Conduct

Be respectful and constructive in all interactions. Help create a welcoming environment for all contributors.