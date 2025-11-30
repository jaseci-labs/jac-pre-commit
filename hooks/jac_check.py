#!/usr/bin/env python
"""Pre-commit hook for type checking Jac files."""

from __future__ import annotations

import sys

from jaclang.compiler.program import JacProgram


def check_file(filepath: str) -> int:
    """Type check a single Jac file.

    Args:
        filepath: Path to the .jac file to check.

    Returns:
        Number of errors found.
    """
    try:
        prog = JacProgram()
        prog.compile(file_path=filepath)

        errors = len(prog.errors_had)
        warnings = len(prog.warnings_had)

        if errors > 0:
            print(f"\n{filepath}:", file=sys.stderr)
            for error in prog.errors_had:
                print(f"  Error: {error}", file=sys.stderr)

        if warnings > 0 and errors == 0:
            # Only show warnings if no errors (to reduce noise)
            for warning in prog.warnings_had:
                print(f"  Warning: {warning}", file=sys.stderr)

        return errors
    except Exception as e:
        print(f"Error checking '{filepath}': {e}", file=sys.stderr)
        return 1


def main() -> int:
    """Entry point for jac-check hook.

    Returns:
        0 if all files pass, 1 if any file has errors.
    """
    if len(sys.argv) < 2:
        print("Usage: jac-check <file.jac> [file2.jac ...]", file=sys.stderr)
        return 0

    total_errors = 0
    files_checked = 0

    for filepath in sys.argv[1:]:
        if filepath.endswith(".jac"):
            total_errors += check_file(filepath)
            files_checked += 1

    if files_checked > 0:
        if total_errors > 0:
            print(
                f"\nType check failed: {total_errors} error(s) in {files_checked} file(s)",
                file=sys.stderr,
            )
            return 1
        else:
            print(f"Type check passed: {files_checked} file(s) checked")

    return 0


if __name__ == "__main__":
    sys.exit(main())
