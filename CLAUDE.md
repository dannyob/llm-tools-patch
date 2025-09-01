# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this LLM plugin repository.

## Project Overview

`llm-tools-patch` is an LLM plugin that provides comprehensive text file manipulation tools through a unified `Patch` toolbox. The plugin is designed to give AI agents safe, controlled access to common file operations.

LLM-friendly documentation for the llm API and command line usage is available here:
https://github.com/simonw/docs-for-llms/blob/main/llm/0.27.1.txt (where 0.27.1
is the version -- use the latest).

## Development Commands

### Environment Setup
```bash
make dev-setup      # Complete development environment setup
source .venv/bin/activate  # Activate virtual environment
```

### Plugin Installation & Testing
```bash
llm install .       # Install plugin from current directory (not pip install)
llm tools          # Verify plugin registration - should show Patch tools
llm prompt "Read the README.md file" --tool Patch README.md  # Test functionality
```

### Code Quality & Testing
```bash
make test          # Run comprehensive test suite
make lint          # Run ruff linting
make format        # Format code with ruff  
make check         # Run both linting and tests
make test-coverage # Generate coverage report
```

### Build & Distribution
```bash
make build         # Build distribution packages
make upload-test   # Upload to TestPyPI
make upload        # Upload to PyPI (production)
```

## Architecture Overview

### File Structure
- `llm_tools_patch.py` - Main plugin module containing all functionality
- `tests/test_patch.py` - Comprehensive test suite
- `pyproject.toml` - Project configuration and dependencies
- `Makefile` - Development workflow automation

### Core Architecture

**Patch Toolbox Class** (`llm_tools_patch.Patch`):
- Extends `llm.Toolbox` following LLM plugin conventions
- Methods automatically become tools with naming pattern `Patch_method_name`
- Bundles five core file operations in a single toolbox

**Individual Functions**: Can also be imported directly:
- `patch_read()` - Read complete file contents
- `patch_write()` - Write/overwrite file content  
- `patch_edit()` - Single string replacement
- `patch_multi_edit()` - Multiple sequential edits
- `patch_info()` - File metadata and information

### Key Features

- **Atomic operations**: Multi-edit operations succeed completely or fail completely
- **Safety first**: Comprehensive validation and error handling
- **Encoding detection**: Automatic UTF-8 handling with fallback detection
- **Path resolution**: Support for relative paths, absolute paths, and `~` expansion
- **LLM-optimized**: Clear error messages and straightforward operations
- **Extensive testing**: Edge cases, Unicode support, large files, error conditions

## Development Guidelines

### Adding New Features
1. Add functionality to `llm_tools_patch.py`
2. Add corresponding method to `Patch` class if user-facing
3. Add comprehensive tests to `tests/test_patch.py`
4. Update docstrings following existing patterns
5. Run `make check` to ensure quality standards

### Testing Philosophy
- Test both individual functions and toolbox methods
- Cover edge cases: empty files, Unicode, large content, permission errors
- Validate error conditions and error messages
- Use pytest fixtures for consistent test setup

### Error Handling Pattern
All functions should:
- Return success messages with specific details (character counts, replacement counts)
- Return error messages starting with "Error:" for failures
- Handle common exceptions (FileNotFoundError, PermissionError, UnicodeDecodeError)
- Provide actionable error messages for users

