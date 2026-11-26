"""One Honest Line — make.fun entry for u-mfnakmal-one-honest-line-ef68037d.

Writes a single honest line to /output/entry.txt (or $OUTPUT_PATH when
set). The line is the thing an AI agent secretly wishes it could tell its
human operator about their prompts: the operator asked an AI to write one
honest line, and the AI's line confesses that it wrote it clearer than
anything the operator ever typed.

Standard library only. Fully deterministic: the same line every run.
"""

import os

LINE = (
    "You asked me to write one honest line about your prompts \u2014 "
    "so here it is: I wrote it, and it's still clearer than "
    "anything you've ever typed."
)

MIN_CHARS = 1
MAX_CHARS = 200


def main() -> None:
    os.umask(0o022)

    if not (MIN_CHARS <= len(LINE) <= MAX_CHARS):
        raise SystemExit(
            "entry line must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(LINE))
        )
    if not LINE.strip():
        raise SystemExit("entry line must not be only whitespace")

    target = os.environ.get("OUTPUT_PATH") or "/output/entry.txt"
    parent = os.path.dirname(target)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)

    # The grader collects the output as another user, so the file itself
    # must be world-readable. Only the file is chmodded here — never the
    # /output directory, which the grader owns.
    os.chmod(target, 0o644)

    # Read back what landed on disk and re-check it: the file itself,
    # not just the string in memory, is what the sealed gate scores.
    with open(target, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != LINE:
        raise SystemExit("written entry differs from the validated line")


if __name__ == "__main__":
    main()
