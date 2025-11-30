#!/usr/bin/env python
"""Pre-commit hook for formatting Jac files."""

from __future__ import annotations

import sys
from pathlib import Path

from jaclang.compiler.program import JacProgram


def format_file(filepath: str) -> bool:
    """Format a single Jac file.

    Args:
        filepath: Path to the .jac file to format.

    Returns:
        True if file was modified, False otherwise.
    """
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File '{filepath}' does not exist.", file=sys.stderr)
        return False

    try:
        original_content = path.read_text()
        formatted_content = JacProgram.jac_file_formatter(str(path))

        if formatted_content != original_content:
            path.write_text(formatted_content)
            print(f"Formatted: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"Error formatting '{filepath}': {e}", file=sys.stderr)
        return False


def main() -> int:
    """Entry point for jac-format hook.

    Returns:
        0 if no files were modified, 1 if files were modified (for pre-commit).
    """
    if len(sys.argv) < 2:
        print("Usage: jac-format <file.jac> [file2.jac ...]", file=sys.stderr)
        return 0

    modified = False
    for filepath in sys.argv[1:]:
        if filepath.endswith(".jac"):
            if format_file(filepath):
                modified = True

    # Return 1 if files were modified so pre-commit knows to re-stage
    return 1 if modified else 0


if __name__ == "__main__":
    sys.exit(main())
