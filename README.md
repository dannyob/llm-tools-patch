# llm-tools-patch

[![PyPI](https://img.shields.io/pypi/v/llm-tools-patch.svg)](https://pypi.org/project/llm-tools-patch/)
[![Changelog](https://img.shields.io/github/v/release/dannyob/llm-tools-patch?include_prereleases&label=changelog)](https://github.com/dannyob/llm-tools-patch/releases)
[![Tests](https://github.com/dannyob/llm-tools-patch/actions/workflows/test.yml/badge.svg)](https://github.com/dannyob/llm-tools-patch/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/dannyob/llm-tools-patch/blob/main/LICENSE)

LLM tools for reading, writing and changing text files 

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/). You'll need at least the [0.26a1 alpha](https://llm.datasette.io/en/latest/changelog.html#a1-2025-05-25).

## Installation

Install this plugin using `llm install`:

```bash
llm install llm-tools-patch
```

Or install from source:

```bash
git clone https://github.com/dannyob/llm-tools-patch
cd llm-tools-patch
llm install .
```

## Usage

This plugin provides tools for text file operations:

- Reading text files
- Writing text files  
- Making targeted changes/patches to text files

Use the `Patch` toolbox in your LLM conversations:

```bash
llm prompt -m gpt-4o-mini "Add a smiley face to the first heading in the README.md file" --tool Patch --chain-limit 0 --ta
```

You'll probably want to use both the `--ta` option (which requires a user confirmation before executing any function) and `--chain-limit 0`, which allows for indefinite tool calls in an `llm` session (`llm`'s default is 5).

## Development

To install for development:

```bash
llm install -e .
```

To run tests:

```bash
make test
```

## Credits and Thanks

Inspired by Claude Code's Read, Edit and MultiEdit tools.
