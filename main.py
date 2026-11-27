#!/usr/bin/env python3
"""Write the missed-deadline excuse (one line, 107 chars) to /output/entry.txt.

Stdlib only. Reads entry.txt sitting next to this script, validates it
against the competition gate (UTF-8 text, 1-200 chars, single line, not
only whitespace), then copies it byte-for-byte to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output) and verifies the copy
by size and sha256.
"""

import hashlib
import os
import sys
from pathlib import Path

ENTRY_NAME = "entry.txt"
MAX_CHARS = 200


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    here = Path(__file__).resolve().parent
    source = here / ENTRY_NAME
    if not source.is_file():
        fail(f"{ENTRY_NAME} not found next to main.py")

    raw = source.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        fail(f"{ENTRY_NAME} is not valid UTF-8")
    if not 1 <= len(text) <= MAX_CHARS:
        fail(f"{ENTRY_NAME} is {len(text)} chars, gate needs 1-{MAX_CHARS}")
    if not text.strip():
        fail(f"{ENTRY_NAME} is only whitespace")
    if "\n" in text:
        fail(f"{ENTRY_NAME} must be a single line")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / ENTRY_NAME
    target.write_bytes(raw)

    check = target.read_bytes()
    if check != raw:
        fail("verification failed: output differs from source")
    digest = hashlib.sha256(raw).hexdigest()
    print(f"wrote {target} ({len(raw)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
