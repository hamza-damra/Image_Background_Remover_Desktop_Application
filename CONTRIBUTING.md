# Contributing to Background Remover

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/bgremover/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - System information (OS, Python version)

### Suggesting Features

1. Check existing feature requests
2. Create an issue with:
   - Clear use case
   - Expected behavior
   - Mockups or examples if applicable

### Code Contributions

#### Setup Development Environment

```powershell
# Clone the repository
git clone https://github.com/yourusername/bgremover.git
cd bgremover

# Run setup
.\setup.ps1

# Create a branch
git checkout -b feature/your-feature-name
```

#### Coding Standards

- Follow PEP 8 style guide
- Add docstrings to functions and classes
- Write unit tests for new features
- Keep commits atomic and well-described

#### Testing

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=bgremover --cov-report=html

# Run specific tests
pytest tests/test_pipeline.py -v
```

#### Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

### Adding Translations

To add a new language:

1. Copy `bgremover/app/ui/i18n/en.json` to `bgremover/app/ui/i18n/<lang>.json`
2. Translate all strings
3. Update `I18n.is_rtl()` if the language is RTL
4. Test the UI with the new language

### Adding Presets

To add a new preset:

1. Edit `bgremover/app/core/presets.py`
2. Add to `BUILTIN_PRESETS` dictionary
3. Test the preset
4. Update documentation

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## Questions?

Feel free to ask questions by:
- Opening an issue
- Starting a discussion
- Reaching out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making Background Remover better! ❤️
