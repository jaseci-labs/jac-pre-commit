#!/usr/bin/env python
"""Pre-commit hook for formatting Jac files."""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

import jaclang.compiler.unitree as uni
from jaclang.compiler.parser import JacParser
from jaclang.compiler.program import JacProgram, format_sched
from jaclang.runtimelib.utils import read_file_with_encoding


class FormatResult:
    """Result of formatting a file."""

    def __init__(
        self,
        filepath: str,
        modified: bool = False,
        error: str | None = None,
        warnings: list[str] | None = None,
    ):
        self.filepath = filepath
        self.modified = modified
        self.error = error
        self.warnings = warnings or []


def format_file(filepath: str) -> FormatResult:
    """Format a single Jac file with full error reporting.

    Args:
        filepath: Path to the .jac file to format.

    Returns:
        FormatResult with status and any errors/warnings.
    """
    path = Path(filepath)
    if not path.exists():
        return FormatResult(filepath, error=f"File does not exist: {filepath}")

    try:
        # Read original content
        original_content = read_file_with_encoding(str(path))

        # Create program and parse
        prog = JacProgram()
        source = uni.Source(original_content, mod_path=str(path))
        parser_pass = JacParser(root_ir=source, prog=prog)
        current_mod = parser_pass.ir_out

        # Check for parse errors before formatting
        if prog.errors_had:
            error_msgs = [str(e) for e in prog.errors_had]
            return FormatResult(
                filepath,
                error=f"Parse errors:\n  " + "\n  ".join(error_msgs),
            )

        # Run format passes
        for pass_cls in format_sched:
            current_mod = pass_cls(ir_in=current_mod, prog=prog).ir_out

        # Check for errors after formatting passes
        if prog.errors_had:
            error_msgs = [str(e) for e in prog.errors_had]
            return FormatResult(
                filepath,
                error=f"Format errors:\n  " + "\n  ".join(error_msgs),
            )

        # Get formatted output
        formatted_content = current_mod.gen.jac

        # Check for empty output (indicates a problem)
        if formatted_content is None or formatted_content.strip() == "":
            # Only error if the original file was not empty
            if original_content.strip():
                return FormatResult(
                    filepath,
                    error="Formatter produced empty output (possible internal error)",
                )
            # Empty file stays empty
            formatted_content = ""

        # Collect warnings
        warnings = [str(w) for w in prog.warnings_had] if prog.warnings_had else []

        # Check if file was modified
        if formatted_content != original_content:
            path.write_text(formatted_content)
            return FormatResult(filepath, modified=True, warnings=warnings)

        return FormatResult(filepath, modified=False, warnings=warnings)

    except Exception as e:
        tb = traceback.format_exc()
        return FormatResult(
            filepath,
            error=f"Unexpected error: {e}\n{tb}",
        )


def main() -> int:
    """Entry point for jac-format hook.

    Returns:
        0 if successful (files may have been modified)
        1 if any errors occurred
    """
    if len(sys.argv) < 2:
        print("Usage: jac-format <file.jac> [file2.jac ...]", file=sys.stderr)
        return 0

    results: list[FormatResult] = []
    for filepath in sys.argv[1:]:
        if filepath.endswith(".jac"):
            results.append(format_file(filepath))

    # Report results
    modified_count = 0
    error_count = 0

    for result in results:
        if result.error:
            print(f"\n❌ {result.filepath}", file=sys.stderr)
            print(f"   {result.error}", file=sys.stderr)
            error_count += 1
        elif result.modified:
            print(f"✓ Formatted: {result.filepath}")
            modified_count += 1
            if result.warnings:
                for w in result.warnings:
                    print(f"  ⚠ {w}", file=sys.stderr)

    # Summary
    if error_count > 0:
        print(
            f"\nFormat failed: {error_count} error(s), {modified_count} file(s) formatted",
            file=sys.stderr,
        )
        return 1

    if modified_count > 0:
        print(f"\n{modified_count} file(s) formatted")
        return 1  # Return 1 so pre-commit knows files changed

    return 0


if __name__ == "__main__":
    sys.exit(main())
