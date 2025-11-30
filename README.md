# Jac Pre-commit Hooks

Production-ready [pre-commit](https://pre-commit.com/) hooks for the [Jac programming language](https://github.com/Jaseci-Labs/jaseci).

## Hooks

| Hook | Description |
|------|-------------|
| `jac-format` | Formats `.jac` files with consistent code style |
| `jac-check` | Runs type checking on `.jac` files |

## Installation

Add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/Jaseci-Labs/jac-pre-commit
    rev: v0.9.3  # Use the latest release tag
    hooks:
      - id: jac-format
      - id: jac-check
```

Then install the hooks:

```bash
pre-commit install
```

## Usage

### Running on All Files

```bash
pre-commit run --all-files
```

### Running Individual Hooks

```bash
# Format only
pre-commit run jac-format --all-files

# Type check only
pre-commit run jac-check --all-files
```

### Running Manually

You can also run the hooks directly:

```bash
# Format a file
jac format myfile.jac

# Type check a file
jac check myfile.jac
```

## Hook Details

### jac-format

Automatically formats Jac source files to maintain consistent code style across your project. Files are modified in place.

- **Modifies files**: Yes (auto-fix)
- **Fails on**: Parse errors

### jac-check

Performs static type analysis on Jac files to catch type errors before runtime.

- **Modifies files**: No
- **Fails on**: Type errors

## Requirements

- Python 3.10+
- [jaclang](https://pypi.org/project/jaclang/) >= 0.9.3

## Development

### Testing Locally

```bash
# Clone the repository
git clone https://github.com/Jaseci-Labs/jac-pre-commit.git
cd jac-pre-commit

# Install in development mode
pip install -e .

# Test against a local jac file
pre-commit try-repo . jac-format --files /path/to/test.jac
pre-commit try-repo . jac-check --files /path/to/test.jac
```

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT License - see [LICENSE](LICENSE) for details.
