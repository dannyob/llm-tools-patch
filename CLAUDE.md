# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Plugin Development Commands

Use `llm install .` to install LLM plugins from the current directory (not pip install).

Test the plugin after installation:
```bash
llm tools  # List available tools to verify registration
llm prompt -m gpt-4o-mini "Please read and modify this config file" --tool Patch  # Test functionality
```

## Architecture Overview

This is an LLM plugin that provides text file manipulation tools through a Toolbox pattern. The plugin exposes file reading, writing, and patching functions bundled in a single `Patch` class.

### Core Components

**Patch** (main toolbox class): Bundles all file manipulation tools
- Extends `llm.Toolbox` 
- Methods become available as tools with naming pattern `Patch_method_name`
- Contains file operations: reading, writing, and making targeted changes to text files

### Key Features

- **Safe file operations**: Read files without modification
- **Targeted patching**: Make specific changes to parts of text files
- **Text-focused**: Designed for configuration files, code, documentation, and other text content
- **LLM-friendly**: Simple interface optimized for AI agent usage