# Contributing to Rearc Data Quest

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [Issues](https://github.com/awolaja/yemi-rearc-Data-Quest/issues) section
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)

### Submitting Changes

1. **Fork the Repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/yemi-rearc-Data-Quest.git
   cd yemi-rearc-Data-Quest
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make Your Changes**
   - Follow the coding standards below
   - Add tests if applicable
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   # Run tests
   python3 -m pytest tests/ -v
   
   # Test the pipeline
   ./run_pipeline.sh
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```
   
   Commit message format:
   - Use present tense ("Add feature" not "Added feature")
   - Be concise but descriptive
   - Reference issues if applicable (#123)

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a PR on GitHub.

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

Example:
```python
def fetch_data(series_id, start_year, end_year):
    """
    Fetch data from BLS API.
    
    Args:
        series_id (str): BLS series identifier
        start_year (str): Start year in YYYY format
        end_year (str): End year in YYYY format
    
    Returns:
        dict: JSON response from API
    """
    # Implementation here
    pass
```

### Documentation

- Update README.md if adding new features
- Add docstrings to new functions
- Update relevant documentation in `docs/`
- Include code comments for complex logic

### Testing

- Write unit tests for new functions
- Ensure existing tests still pass
- Aim for good test coverage
- Test files should be in `tests/` directory
- Name test files as `test_<module>.py`

Example test:
```python
def test_fetch_data_returns_dict():
    """Test that fetch_data returns a dictionary"""
    result = fetch_data('CES0000000001', '2023', '2023')
    assert isinstance(result, dict)
```

## Development Setup

1. Clone the repository
2. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest  # for testing
   ```

## Areas for Contribution

We welcome contributions in these areas:

### Features
- Support for multiple BLS series simultaneously
- Database integration (PostgreSQL, MySQL)
- Cloud storage integration (AWS S3, Google Cloud Storage)
- Data visualization dashboards
- Email/Slack notifications
- Incremental data updates
- Additional data sources

### Improvements
- Better error handling
- Performance optimizations
- More comprehensive tests
- Enhanced documentation
- Code refactoring

### Bug Fixes
- Fix reported issues
- Improve error messages
- Handle edge cases

## Pull Request Process

1. Update documentation to describe your changes
2. Add tests for new functionality
3. Ensure all tests pass
4. Update the README if needed
5. Request review from maintainers
6. Address review feedback
7. Once approved, your PR will be merged

## Questions?

If you have questions:
- Check the [documentation](docs/)
- Open an issue for discussion
- Contact the maintainers

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing! 🎉
