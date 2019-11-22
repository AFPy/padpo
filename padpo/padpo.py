import argparse
import sys
import tempfile
from pathlib import Path

import requests
import simplelogging

from padpo.pofile import PoFile
from padpo.checkers import checkers


log = None


def check_file(path, pull_request_info=None):
    file = PoFile(path)

    for checker in checkers:
        checker.check_file(file)

    return file.display_warnings(pull_request_info)


def check_directory(path, pull_request_info=None):
    path = Path(path)
    any_error = False
    for file in path.rglob("*.po"):
        any_error = check_file(file, pull_request_info) or any_error
    return any_error


def check_path(path, pull_request_info=None):
    path = Path(path)
    if path.is_dir():
        return check_directory(path, pull_request_info)
    else:
        return check_file(path, pull_request_info)


class PullRequestInfo:
    def __init__(self):
        self._data = {}

    def add_file(self, filename, temp_path, diff):
        self._data[str(temp_path)] = (temp_path, diff, filename)

    def diff(self, path):
        if str(path) in self._data:
            return self._data[str(path)][1]
        return ""

    def temp_path(self, path):
        if str(path) in self._data:
            return self._data[str(path)][0]
        return ""

    def filename(self, path):
        if str(path) in self._data:
            return self._data[str(path)][2]
        return ""


def pull_request_files(pull_request):
    pull_request = pull_request.replace("/pull/", "/pulls/")
    request = requests.get(
        f"https://api.github.com/repos/{pull_request}/files"
    )
    request.raise_for_status()
    # TODO remove directory at end of execution
    temp_dir = tempfile.mkdtemp(prefix="padpo_")
    pr = PullRequestInfo()
    for file in request.json():
        filename = file["filename"]
        temp_file = Path(temp_dir) / filename
        content_request = requests.get(file["raw_url"])
        content_request.raise_for_status()
        temp_file_dir = temp_file.parent
        temp_file_dir.mkdir(parents=True, exist_ok=True)
        temp_file.write_bytes(content_request.content)
        pr.add_file(filename, temp_file, file["patch"])
    return temp_dir, pr


def main():
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
        path, pull_request_info = pull_request_files(pull_request)

    any_error = check_path(path, pull_request_info=pull_request_info)
    if any_error:
        sys.exit(1)
