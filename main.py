#!/usr/bin/env python3
"""Two Lines to Your Past Self — entry writer.

Emits exactly two lines of plain text to /output/entry.txt:
line one warns the writer's past self about one specific moment,
line two says in one sentence why that moment mattered and what
changed because of it. The whole text stays within 280 characters.
"""

import os
import re
import sys

# Abbreviations whose periods do not end a sentence.
_ABBREVIATIONS = ("p.m.", "a.m.", "e.g.", "i.e.", "Mr.", "Mrs.", "Dr.")

_SENTENCE_END = re.compile(r"[.!?](?=\s|$)")

LINE_ONE = (
    "Don't tell your mother 'I'll call you back' at 9:03 p.m. "
    "the night before her surgery, then fall asleep with the phone "
    "in your hand."
)
LINE_TWO = (
    "It was the last thing she ever asked of you, and you have "
    "answered every call on the first ring since."
)


def count_sentences(line: str) -> int:
    """Count sentences in one line, ignoring periods inside abbreviations."""
    masked = line
    for abbr in _ABBREVIATIONS:
        masked = masked.replace(abbr, abbr.replace(".", "\x00"))
    return len(_SENTENCE_END.findall(masked))


def build_entry() -> str:
    first = " ".join(LINE_ONE.split())
    second = " ".join(LINE_TWO.split())
    if first == second:
        raise ValueError("line two must not restate line one")
    for line in (first, second):
        if count_sentences(line) != 1:
            raise ValueError(f"each line must be exactly one sentence: {line!r}")
        if not line.endswith("."):
            raise ValueError("each line must be one complete sentence")
    text = first + "\n" + second
    if not 1 <= len(text) <= 280:
        raise ValueError(f"entry is {len(text)} chars, must be 1-280")
    if text.count("\n") != 1:
        raise ValueError("entry must be exactly two lines")
    return text


def main() -> int:
    text = build_entry()
    outdir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print(f"wrote {len(text)} chars, 2 lines, to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
