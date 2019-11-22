"""Entry point of padpo."""

import argparse
import sys
from pathlib import Path

import simplelogging

from padpo.pofile import PoFile
from padpo.checkers import checkers
from padpo.github import pull_request_files


log = None


def check_file(path, pull_request_info=None):
    """Check a `*.po` file."""
    pofile = PoFile(path)

    for checker in checkers:
        checker.check_file(pofile)

    return pofile.display_warnings(pull_request_info)


def check_directory(path, pull_request_info=None):
    """Check a directory containing `*.po` files."""
    path = Path(path)
    any_error = False
    for filepath in path.rglob("*.po"):
        any_error = check_file(filepath, pull_request_info) or any_error
    return any_error


def check_path(path, pull_request_info=None):
    """Check a path (`*.po` file or directory)."""
    path = Path(path)
    if path.is_dir():
        return check_directory(path, pull_request_info)
    else:
        return check_file(path, pull_request_info)


def main():
    """Entry point."""
    global log
    log = simplelogging.get_logger("__main__")

    parser = argparse.ArgumentParser(description="Linter for *.po files.")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    files = parser.add_mutually_exclusive_group(required=True)
    files.add_argument(
        "-i",
        "--input-path",
        metavar="PATH",
        type=str,
        help="path of the file or directory to check",
        default="",
    )
    files.add_argument(
        "-g",
        "--github",
        metavar="python/python-docs-fr/pull/978",
        type=str,
        help="path of pull request in GitHub to check",
        default="",
    )
    files.add_argument(
        "-p",
        "--python-docs-fr",
        metavar="978",
        type=int,
        help="ID of pull request in python-docs-fr repository",
        default=0,
    )
    args = parser.parse_args()
    if args.verbose < 1:
        log.reduced_logging()
    elif args.verbose < 2:
        log.normal_logging()
    else:
        log.full_logging()

    if args.input_path:
        path = args.input_path
        pull_request_info = None
    else:
        pull_request = ""
        if args.github:
            pull_request = args.github
        if args.python_docs_fr:
            pull_request = f"python/python-docs-fr/pull/{args.python_docs_fr}"
        pull_request_info = pull_request_files(pull_request)
        path = pull_request_info.download_directory

    any_error = check_path(path, pull_request_info=pull_request_info)
    if any_error:
        sys.exit(1)
