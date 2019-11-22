"""Managment of `*.po` files."""

import re

import simplelogging

log = simplelogging.get_logger()


class PoItem:
    def __init__(self, path, lineno):
        self.path = path[3:]
        self.lineno_start = lineno
        self.lineno_end = lineno
        self.parsing_msgid = None
        self.msgid = []
        self.msgstr = []
        self.fuzzy = False
        self.warnings = []
        self.inside_pull_request = False

    def append_line(self, line):
        self.lineno_end += 1
        if line.startswith("msgid"):
            self.parsing_msgid = True
            self.msgid.append(line[7:-2])
        elif line.startswith("msgstr"):
            self.parsing_msgid = False
            self.msgstr.append(line[8:-2])
        elif line.startswith("#, fuzzy"):
            self.fuzzy = True
        elif line.startswith('"'):
            if self.parsing_msgid:
                self.msgid.append(line[1:-2])
            elif not self.parsing_msgid is None:
                self.msgstr.append(line[1:-2])

    def __str__(self):
        return (
            f"    - {self.msgid_full_content}\n"
            f"        => {self.msgstr_full_content}\n"
            f"        => {self.msgstr_rst2txt}\n"
        )

    @property
    def msgid_full_content(self):
        return "".join(self.msgid)

    @property
    def msgstr_full_content(self):
        return "".join(self.msgstr)

    @property
    def msgid_rst2txt(self):
        return self.rst2txt(self.msgid_full_content)

    @property
    def msgstr_rst2txt(self):
        return self.rst2txt(self.msgstr_full_content)

    @staticmethod
    def rst2txt(text):
        text = re.sub(r"::", r":", text)
        text = re.sub(r"``(.*?)``", r"« \1 »", text)
        text = re.sub(r"\"(.*?)\"", r"« \1 »", text)
        text = re.sub(r":pep:`(.*?)`", r"PEP \1", text)
        text = re.sub(r":[a-z:]+:`(.+?)`", r"« \1 »", text)
        text = re.sub(r"\*\*(.*?)\*\*", r"« \1 »", text)
        text = re.sub(
            r"\*(.*?)\*", r"« \1 »", text
        )  # TODO sauf si déjà entre «»
        return text

    def add_warning(self, checker_name: str, text: str) -> None:
        self.warnings.append(Warning(checker_name, text))

    def add_error(self, checker_name: str, text: str) -> None:
        self.warnings.append(Error(checker_name, text))


class PoFile:
    def __init__(self, path=None):
        self.content: List[PoItem] = []
        self.path = path
        if path:
            self.parse_file(path)

    def parse_file(self, path):
        # TODO assert path is a file, not a dir
        item = None
        with open(path, encoding="utf8") as f:
            for lineno, line in enumerate(f):
                if line.startswith("#: "):
                    if item:
                        self.content.append(item)
                    item = PoItem(line, lineno + 1)
                elif item:
                    item.append_line(line)
        if item:
            self.content.append(item)

    def __str__(self):
        ret = f"Po file: {self.path}\n"
        ret += "\n".join(str(item) for item in self.content)
        return ret

    def rst2txt(self):
        return "\n\n".join(item.msgstr_rst2txt for item in self.content)

    def display_warnings(self, pull_request_info=None):
        self.tag_in_pull_request(pull_request_info)
        any_error = False
        for item in self.content:
            if not item.inside_pull_request:
                continue
            prefix = f"{self.path}:{item.lineno_start:-4} %s"
            log.debug(prefix, "")
            for message in item.warnings:
                if isinstance(message, Error):
                    log.error(prefix, message)
                    any_error = True
                elif isinstance(message, Warning):
                    log.warning(prefix, message)
        return any_error

    def tag_in_pull_request(self, pull_request_info):
        if not pull_request_info:
            for item in self.content:
                item.inside_pull_request = True
        else:
            diff = pull_request_info.diff(self.path)
            for item in self.content:
                item.inside_pull_request = False
            for lineno_diff in self.lines_in_diff(diff):
                for item in self.content:
                    if item.lineno_start <= lineno_diff <= item.lineno_end:
                        item.inside_pull_request = True

    @staticmethod
    def lines_in_diff(diff):
        for line in diff.splitlines():
            if line.startswith("@@"):
                m = re.search(r"@@\s*\-\d+,\d+\s+\+(\d+),(\d+)\s+@@", line)
                if m:
                    line_start = int(m.group(1))
                    nb_lines = int(m.group(2))
                    # github add 3 extra lines around diff info
                    extra_info_lines = 3
                    for lineno in range(
                        line_start + extra_info_lines,
                        line_start + nb_lines - extra_info_lines,
                    ):
                        yield lineno


class Message:
    def __init__(self, checker_name: str, text: str):
        self.checker_name = checker_name
        self.text = text

    def __str__(self):
        return f"[{self.checker_name:^14}] {self.text}"


class Warning(Message):
    pass


class Error(Message):
    pass
