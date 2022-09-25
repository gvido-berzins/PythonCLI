import argparse
from pathlib import Path
import tempfile
from typing import Sequence
import sys
import zipfile

import mpv


def main(argv: list[Sequence]) -> int:
    args = parse_args(argv)
    if args.path.is_dir():
        paths = args.path.glob("*.zip")
    elif args.path.is_file():
        paths = [args.path]
    else:
        print("Not a file or directory", file=sys.stderr)
        return 1

    allresults = []
    for path in paths:
        results = find_file_in_zip(args.search, path, args.first)
        allresults.extend(results)

    for result in allresults:
        print(f"Found {result[1]} in {result[0]}")
        if args.view:
            try:

                view_zip_file_content(result[0], result[1])
            except KeyboardInterrupt:
                print("Exiting...")
                return 0
            except Exception as e:
                print(e, file=sys.stderr)
                return 1

    return 0


def parse_args(argv: list[Sequence]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Find a file in a multiple archive files. Supported archive formats: ".zip".'
    )
    parser.add_argument("-s", "--search", help="Search string.", required=True)
    parser.add_argument(
        "-p",
        "--path",
        type=path_type,
        help="Path to a file or directory or archive files.",
        required=True,
    )
    parser.add_argument(
        "--view", default=False, action="store_true", help="View the archive file."
    )
    parser.add_argument(
        "--first",
        default=False,
        action="store_true",
        help="Get only the first archive file.",
    )
    return parser.parse_args(argv)


def path_type(path: str) -> Path:
    return Path(path).expanduser().resolve()


def find_file_in_zip(
    search: str, path: Path, first: bool = False
) -> list[tuple[str, str]]:
    """Find a file in a zip archive."""
    results = []
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if search in info.filename:
                results.append((path, info.filename))
                if first is True:
                    break
    return results


def view_zip_file_content(path: str, filename: str) -> None:
    """View a file in a zip archive with mpv."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(path) as zf:
            zf.extract(filename, tmpdir)
            print(f"Viewing {filename} in {path}")
            view_file(Path(tmpdir) / filename)


def view_file(path: Path) -> None:
    """View a file with mpv."""
    if path.suffix not in (".mkv", ".mp4", ".webm"):
        print(f"Unsupported file type {path.suffix}")
        return
    player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True)
    player.play(str(path))
    try:
        player.wait_for_playback()
    except Exception:
        player.terminate()


def patched_main() -> None:
    """Main function used for CLI interface."""
    raise SystemExit(main(sys.argv[1:]))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
