"""Managment of `*.po` files."""

import re
from typing import List
from polib import pofile

import simplelogging

log = simplelogging.get_logger()


class PoItem:
    """Translation item."""

    def __init__(self, entry):
        """Initializer."""
        self.warnings = []
        self.inside_pull_request = False
        self.entry = entry


    def __str__(self):
        """Return string representation."""
        return (
            f"    - {self.entry.msgid}\n"
            f"        => {self.entry.msgstr}\n"
            f"        => {self.msgstr_rst2txt}\n"
        )


    @property
    def msgid_rst2txt(self):
        """Full content of the msgid (reStructuredText escaped)."""
        return self.rst2txt(self.entry.msgid)

    @property
    def msgstr_rst2txt(self):
        """Full content of the msgstr (reStructuredText escaped)."""
        return self.rst2txt(self.entry.msgstr)

    @staticmethod
    def rst2txt(text):
        """
        Escape reStructuredText markup.

        The text is modified to transform reStructuredText markup
        in textual version. For instance:

        * "::" becomes ":"
        * ":class:`PoFile`" becomes "« PoFile »"
        """
        text = re.sub(r"::", r":", text)
        text = re.sub(r"``(.*?)``", r"« \1 »", text)
        text = re.sub(r"\"(.*?)\"", r"« \1 »", text)
        text = re.sub(r":[Pp][Ee][Pp]:`(.*?)`", r"PEP \1", text)
        text = re.sub(r":[a-zA-Z:]+:`(.+?)`", r"« \1 »", text)
        text = re.sub(r"\*\*(.*?)\*\*", r"« \1 »", text)
        text = re.sub(r"\*(.*?)\*", r"« \1 »", text)  # TODO sauf si déjà entre «»
        text = re.sub(r"`(.*?)\s*<((?:http|https|ftp)://.*?)>`_", r"\1 (« \2 »)", text)
        text = re.sub(r"<((?:http|https|ftp)://.*?)>", r"« \1 »", text)
        return text

    def add_warning(self, checker_name: str, text: str) -> None:
        """Add a checker warning to the item."""
        self.warnings.append(Warning(checker_name, text))

    def add_error(self, checker_name: str, text: str) -> None:
        """Add a checker error to the item."""
        self.warnings.append(Error(checker_name, text))


class PoFile:
    """A `*.po` file information."""

    def __init__(self, path=None):
        """Initializer."""
        self.content: List[PoItem] = []
        self.path = path
        if path:
            self.parse_file(path)

    def parse_file(self, path):
        """Parse a `*.po` file according to its path."""
        # TODO assert path is a file, not a dir
        self.pofile = pofile(path)
        for entry in self.pofile:
            item = PoItem(entry)
            self.content.append(item)

        # lineno_end only needed for github patch. May be removed ?
        import sys
        lineno_end = sys.maxsize
        for item in sorted(self.content, key=lambda x: x.entry.linenum, reverse=True):
            item.lineno_end = lineno_end
            lineno_end = item.entry.linenum - 1


    def __str__(self):
        """Return string representation."""
        ret = f"Po file: {self.path}\n"
        ret += "\n".join(str(item) for item in self.content)
        return ret

    def rst2txt(self):
        """Escape reStructuredText markup."""
        return "\n\n".join(item.msgstr_rst2txt for item in self.content)

    def display_warnings(self, pull_request_info=None):
        """Log warnings and errors, return errors and warnings lists."""
        self.tag_in_pull_request(pull_request_info)
        errors = []
        warnings = []
        for item in self.content:
            if not item.inside_pull_request:
                continue
            for message in item.warnings:
                if isinstance(message, Error):
                    log.error(
                        message.text,
                        extra={
                            "pofile": self.path,
                            "poline": item.entry.linenum,
                            "checker": message.checker_name,
                            "leveldesc": "error",
                        },
                    )
                    errors.append(message)
                elif isinstance(message, Warning):
                    log.warning(
                        message.text,
                        extra={
                            "pofile": self.path,
                            "poline": item.entry.linenum,
                            "checker": message.checker_name,
                            "leveldesc": "warning",
                        },
                    )
                    warnings.append(message)
        return errors, warnings

    def tag_in_pull_request(self, pull_request_info):
        """Tag items being part of the pull request."""
        if not pull_request_info:
            for item in self.content:
                item.inside_pull_request = True
        else:
            diff = pull_request_info.diff(self.path)
            for item in self.content:
                item.inside_pull_request = False
            for lineno_diff in self.lines_in_diff(diff):
                for item in self.content:
                    if item.entry.linenum <= lineno_diff <= item.lineno_end:
                        item.inside_pull_request = True

    @staticmethod
    def lines_in_diff(diff):
        """Yield line numbers modified in a diff (new line numbers)."""
        for line in diff.splitlines():
            if line.startswith("@@"):
                match = re.search(r"@@\s*\-\d+,\d+\s+\+(\d+),(\d+)\s+@@", line)
                if match:
                    line_start = int(match.group(1))
                    nb_lines = int(match.group(2))
                    # github add 3 extra lines around diff info
                    extra_info_lines = 3
                    for lineno in range(
                        line_start + extra_info_lines,
                        line_start + nb_lines - extra_info_lines,
                    ):
                        yield lineno


class Message:
    """Checker message."""

    def __init__(self, checker_name: str, text: str):
        """Initializer."""
        self.checker_name = checker_name
        self.text = text

    def __str__(self):
        """Return string representation."""
        return f"[{self.checker_name:^14}] {self.text}"


class Warning(Message):
    """Checker warning message."""


class Error(Message):
    """Checker error message."""
