"""Entry point of padpo."""

import argparse
import pkg_resources
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
    result_errors = []
    result_warnings = []
    for filepath in path.rglob("*.po"):
        errors, warnings = check_file(filepath, pull_request_info)
        result_errors.extend(errors)
        result_warnings.extend(warnings)
    return result_errors, result_warnings


def check_path(path, pull_request_info=None):
    """Check a path (`*.po` file or directory)."""
    path = Path(path)
    if path.is_dir():
        return check_directory(path, pull_request_info)
    else:
        return check_file(path, pull_request_info)


def check_paths(paths, pull_request_info=None):
    """Check a list of paths (`*.po` file or directory)."""
    result_errors = []
    result_warnings = []
    for path in paths:
        errors, warnings = check_path(path, pull_request_info)
        result_errors.extend(errors)
        result_warnings.extend(warnings)
    return result_errors, result_warnings


def main():
    """Entry point."""
    global log

    parser = argparse.ArgumentParser(description="Linter for *.po files.")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    files = parser.add_mutually_exclusive_group(required=True)
    files.add_argument(
        "-i",
        "--input-path",
        metavar="PATH",
        type=str,
        help="path of the file or directory to check",
        default=[],
        # allow the user to provide no path at all,
        # this helps writing scripts
        nargs="*",
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
    files.add_argument("--version", action="store_true", help="Return version")
    parser.add_argument("-c", "--color", action="store_true", help="color output")
    args = parser.parse_args()

    if args.version:
        print(pkg_resources.get_distribution("padpo").version)
        sys.exit(0)

    if args.color:
        console_format = (
            "%(log_color)s[%(levelname)-8s]%(reset)s "
            "%(green)s%(pofile)s:%(poline)s: "
            "%(cyan)s[%(checker)s] %(message)s%(reset)s"
        )
    else:
        console_format = "%(pofile)s:%(poline)s: %(leveldesc)s: %(message)s"
    log = simplelogging.get_logger("__main__", console_format=console_format)

    if args.verbose < 1:
        log.reduced_logging()
    elif args.verbose < 2:
        log.normal_logging()
    else:
        log.full_logging()

    if args.github or args.python_docs_fr:
        pull_request = ""
        if args.github:
            pull_request = args.github
        if args.python_docs_fr:
            pull_request = f"python/python-docs-fr/pull/{args.python_docs_fr}"
        pull_request_info = pull_request_files(pull_request)
        path = [pull_request_info.download_directory]
    else:
        path = args.input_path
        pull_request_info = None

    errors, warnings = check_paths(path, pull_request_info=pull_request_info)
    if errors:
        sys.exit(1)
