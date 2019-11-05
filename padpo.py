import argparse
import json
import re
import subprocess
import sys
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path

import simplelogging

# log = simplelogging.get_logger(console_level=simplelogging.DEBUG)
log = simplelogging.get_logger()


class PoItem:
    def __init__(self, path, lineno):
        self.path = path[3:]
        self.lineno = lineno
        self.parsing_msgid = None
        self.msgid = []
        self.msgstr = []
        self.fuzzy = False
        self.warnings = []

    def append_line(self, line):
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
        text = re.sub(r":pep:`(.*?)`", r"PEP \1", text)
        for term in (
            "attr",
            "class",
            "const",
            "data",
            "dfn",
            "exc",
            "file",
            "func",
            "keyword",
            "meth",
            "mod",
            "ref",
            "source",
            "term",
        ):
            text = re.sub(rf":{term}:`(.*?)`", r"« \1 »", text)
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
        self.content = []
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

    def display_warnings(self):
        any_error = False
        for item in self.content:
            prefix = f"{self.path}:{item.lineno:-4} %s"
            log.debug(prefix, "")
            for message in item.warnings:
                if isinstance(message, Error):
                    log.error(prefix, message)
                    any_error = True
                elif isinstance(message, Warning):
                    log.warning(prefix, message)
        return any_error


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


class Checker(ABC):
    def __init__(self, name):
        self.name = name

    def check_file(self, pofile: PoFile):
        if not isinstance(pofile, PoFile):
            log.error("%s is not an instance of PoFile", str(pofile))
        for item in pofile.content:
            self.check_item(item)

    @abstractmethod
    def check_item(self, item: PoItem):
        pass


class DoubleSpaceChecker(Checker):
    def __init__(self):
        super().__init__(name="Double space")

    def check_item(self, item: PoItem):
        for match in re.finditer(
            r"(.{0,30})\s\s(.{0,30})", item.msgstr_full_content
        ):
            item.add_warning(
                self.name,
                f"Double spaces detected between ###{match.group(1)}### and ###{match.group(2)}###",
            )


class LineLengthChecker(Checker):
    def __init__(self):
        super().__init__(name="Line length")

    def check_item(self, item: PoItem):
        for line in item.msgstr:
            if len(line) > 77:  # 77 + 2 ("")
                item.add_error(
                    self.name, f"Line too long ({len(line) + 2} > 79): {line}"
                )


class FuzzyChecker(Checker):
    def __init__(self):
        super().__init__(name="Fuzzy")

    def check_item(self, item: PoItem):
        if item.fuzzy:
            item.add_warning(self.name, "This entry is tagged as fuzzy.")


class EmptyChecker(Checker):
    def __init__(self):
        super().__init__(name="Empty")

    def check_item(self, item: PoItem):
        if not item.msgstr_full_content and item.msgid_full_content:
            item.add_warning(self.name, "This entry is not translated yet.")


def replace_quotes(match):
    length = len(match.group(0)) - 4
    return "« " + length * "x" + " »"


class NonBreakableSpaceChecker(Checker):
    def __init__(self):
        super().__init__(name="NBSP")

    def check_item(self, item: PoItem):

        text = item.msgstr_rst2txt
        for match in re.finditer(r"(.{0,30})(«[^ ])(.{0,30})", text):
            self.__add_message(item, *match.groups())
        for match in re.finditer(r"(.{0,30})([^ ][»])(.{0,30})", text):
            self.__add_message(item, *match.groups())
        text = re.sub(r"«\s(.*?)\s»", replace_quotes, text)
        text = re.sub(r"http://", "http-//", text)
        text = re.sub(r"https://", "https-//", text)
        for sign in "?!:;":
            regex = r"(.{0,30})([^ ][" + sign + r"])(.{0,30})"
            for match in re.finditer(regex, text):
                prefix = item.msgstr_rst2txt[match.start(1) : match.end(1)]
                suffix = item.msgstr_rst2txt[match.start(3) : match.end(3)]
                match = item.msgstr_rst2txt[match.start(2) : match.end(2)]
                self.__add_message_space_before(item, prefix, match, suffix)

    def __add_message(self, item, prefix, match, suffix):
        item.add_error(
            self.name,
            f'Space should be replaced with a non-breakable space in "{match}": between ###{prefix}### and ###{suffix}###',
        )

    def __add_message_space_before(self, item, prefix, match, suffix):
        item.add_error(
            self.name,
            f'There should be a non-breakable space before "{match[1:]}": between ###{prefix}### and ###{match[1:]}{suffix}###',
        )


class GrammalecteChecker(Checker):
    def __init__(self):
        super().__init__(name="Grammalecte")
        self.dir = None

    def check_file(self, pofile: PoFile):
        if not isinstance(pofile, PoFile):
            log.error("%s is not an instance of PoFile", str(pofile))
        fd, name = tempfile.mkstemp(suffix=".txt", prefix="padpo_", text=True)
        with open(name, "w", encoding="utf8") as f:
            text = pofile.rst2txt()
            text = re.sub(r"«\s(.*?)\s»", replace_quotes, text)
            f.write(text)
        result = subprocess.run(
            [
                "grammalecte-cli.py",
                "-f",
                name,
                "-off",
                "apos",
                "--json",
                "--only_when_errors",
            ],
            capture_output=True,
            text=True,
        )
        if result.stdout:
            warnings = json.loads(result.stdout)
            for warning in warnings["data"]:
                for error in warning["lGrammarErrors"]:
                    if self.filter_out(error):
                        continue
                    item_index = int(warning["iParagraph"]) // 2
                    item = pofile.content[item_index]
                    start = max(0, int(error["nStart"]) - 40)
                    end = max(0, int(error["nEnd"]) + 10)
                    item.add_warning(
                        self.name,
                        # self.name + " " + error["sRuleId"],  # TODO
                        error["sMessage"]
                        + " => ###"
                        + item.msgstr_rst2txt[start:end]
                        + "###",
                    )

    def check_item(self, item: PoItem):
        pass

    def filter_out(self, error):
        msg = error["sRuleId"]
        if msg == "esp_milieu_ligne":
            return True  # double space
        if msg == "nbsp_avant_deux_points":
            return True
        if msg == "nbsp_avant_double_ponctuation":
            return True
        return False


checkers = [
    DoubleSpaceChecker(),
    LineLengthChecker(),
    FuzzyChecker(),
    EmptyChecker(),
    NonBreakableSpaceChecker(),
    GrammalecteChecker(),
]


def check_file(path):
    file = PoFile(path)

    for checker in checkers:
        checker.check_file(file)

    return file.display_warnings()


def check_directory(path):
    path = Path(path)
    any_error = False
    for file in path.rglob("*.po"):
        any_error = check_file(file) or any_error
    return any_error


def check_path(path):
    path = Path(path)
    if path.is_dir():
        return check_directory(path)
    else:
        return check_file(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Linter for *.po files.")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument(
        "path",
        metavar="PATH",
        type=str,
        help="path of the file or directory to check",
    )
    args = parser.parse_args()
    if args.verbose < 1:
        log.reduced_logging()
    elif args.verbose < 2:
        log.normal_logging()
    else:
        log.full_logging()

    any_error = check_path(args.path)
    if any_error:
        sys.exit(1)
