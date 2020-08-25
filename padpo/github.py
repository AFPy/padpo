"""GitHub interactions."""

import tempfile
from pathlib import Path

import requests
import simplelogging

log = simplelogging.get_logger()


class PullRequestInfo:
    """Information on a pull request."""

    def __init__(self):
        """Initializer."""
        self._data = {}
        self.download_directory = None

    def add_file(self, filename, temp_path, diff):
        """Add file info to the pull request."""
        self._data[str(temp_path)] = (temp_path, diff, filename)

    def diff(self, path):
        """Return diff of a file in the pull request."""
        if str(path) in self._data:
            return self._data[str(path)][1]
        return ""

    def temp_path(self, path):
        """Return temporary file path of the file in the pull request."""
        if str(path) in self._data:
            return self._data[str(path)][0]
        return ""

    def filename(self, path):
        """Return file name of a file in the pull request."""
        if str(path) in self._data:
            return self._data[str(path)][2]
        return ""


def pull_request_files(pull_request: str):
    """Return pull request information."""
    pull_request = pull_request.replace("/pull/", "/pulls/")
    request = requests.get(f"https://api.github.com/repos/{pull_request}/files")
    request.raise_for_status()
    # TODO remove directory at end of execution
    temp_dir = tempfile.mkdtemp(prefix="padpo_")
    pr = PullRequestInfo()
    pr.download_directory = temp_dir
    for fileinfo in request.json():
        filename = fileinfo["filename"]
        temp_file = Path(temp_dir) / filename
        content_request = requests.get(fileinfo["raw_url"])
        content_request.raise_for_status()
        temp_file_dir = temp_file.parent
        temp_file_dir.mkdir(parents=True, exist_ok=True)
        temp_file.write_bytes(content_request.content)
        if "patch" in fileinfo:
            # if a patch is provided (patch is small enough)
            pr.add_file(filename, temp_file, fileinfo["patch"])
    return pr
