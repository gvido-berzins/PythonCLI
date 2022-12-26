#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", type=lambda p: Path(p).expanduser().resolve(), help="File to dedupe."
    )
    parser.add_argument("-s", "--stdout", action="store_true", help="Print to stdout.")
    parser.add_argument(
        "-o",
        "--outfile",
        default=Path.cwd() / "deduped",
        type=lambda p: Path(p).expanduser().resolve(),
        help="Output of the deduped contents.",
    )
    args = parser.parse_args()
    return dedupe(args.infile, args.outfile, args.stdout)


def dedupe(infile: Path, outfile: Path | None, stdout: bool = False) -> int:
    if outfile is None and stdout is False:
        print("'outfile' can't be None when 'stdout' is False", sys.stderr)
        return 1

    seenlines = []

    def add(l: str) -> str | None:
        seenlines.append(l)
        return l

    newtext = "\n".join(
        filter(
            None,
            (
                add(l)
                for l in infile.read_text().splitlines(keepends=False)
                if l not in seenlines
            ),
        )
    )

    if stdout is False:
        outfile.write_text(newtext)
    else:
        print(newtext)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
