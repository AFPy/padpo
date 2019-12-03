"""Checker for grammar errors."""

import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Set
from zipfile import ZipFile

import requests
import simplelogging

from padpo.checkers.baseclass import Checker, replace_quotes
from padpo.pofile import PoItem, PoFile

log = simplelogging.get_logger()


class GrammalecteChecker(Checker):
    """Checker for grammar errors."""

    name = "Grammalecte"

    def __init__(self):
        """Initialiser."""
        super().__init__()
        self.dir = None
        self.personal_dict: Set[str] = set()
        self.get_personal_dict()

    @staticmethod
    def run_grammalecte(filename: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                "grammalecte-cli.py",
                "-f",
                filename,
                "-off",
                "apos",
                "--json",
                "--only_when_errors",
            ],
            capture_output=True,
            text=True,
        )

    def check_file(self, pofile: PoFile):
        """Check a `*.po` file."""
        if not isinstance(pofile, PoFile):
            log.error("%s is not an instance of PoFile", str(pofile))
        _, filename = tempfile.mkstemp(
            suffix=".txt", prefix="padpo_", text=True
        )
        with open(filename, "w", encoding="utf8") as f:
            text = pofile.rst2txt()
            text = re.sub(r"«\s(.*?)\s»", replace_quotes, text)
            f.write(text)
        try:
            result = self.run_grammalecte(filename)
        except FileNotFoundError as e:
            if e.filename == "grammalecte-cli.py":
                install_grammalecte()
                result = self.run_grammalecte(filename)
        if result.stdout:
            warnings = json.loads(result.stdout)
            self.manage_grammar_errors(warnings, pofile)
            self.manage_spelling_errors(warnings, pofile)
        Path(filename).unlink()

    def check_item(self, item: PoItem):
        """Check an item in a `*.po` file (does nothing)."""
        pass

    def manage_grammar_errors(self, warnings, pofile: PoFile):
        """Manage grammar errors returned by grammalecte."""
        for warning in warnings["data"]:
            for error in warning["lGrammarErrors"]:
                if self.filter_out_grammar_error(error):
                    continue
                item_index = int(warning["iParagraph"]) // 2
                item = pofile.content[item_index]
                start = max(0, int(error["nStart"]) - 40)
                end = max(0, int(error["nEnd"]) + 10)
                item.add_warning(
                    self.name,
                    f'{error["sMessage"]} => '
                    f"###{item.msgstr_rst2txt[start:end]}###",
                )

    def filter_out_grammar_error(self, error):
        """Return True when grammalecte error should be ignored."""
        msg = error["sRuleId"]
        if msg in (
            "esp_milieu_ligne",  # double space
            "nbsp_avant_deux_points",  # NBSP
            "nbsp_avant_double_ponctuation",  # NBSP
        ):
            return True
        if "typo_guillemets_typographiques_simples" in msg:
            return True  # ignore ' quotes
        msg_text = error["sMessage"]
        if msg_text in (
            "Accord de genre erroné : « ABC » est masculin.",
            "Accord de genre erroné : « PEP » est masculin.",
            "Accord de nombre erroné : « PEP » devrait être au pluriel.",
            "Accord de genre erroné : « une entrée » est féminin, « utilisateur » est masculin.",
        ):
            return True
        if "S’il s’agit d’un impératif" in msg_text:
            if error["nStart"] == 0:
                # ignore imperative conjugation at begining of 1st sentence
                return True
        return False

    def manage_spelling_errors(self, warnings, pofile: PoFile):
        """Manage spelling errors returned by grammalecte."""
        for warning in warnings["data"]:
            for error in warning["lSpellingErrors"]:
                if self.filter_out_spelling_error(error):
                    continue
                item_index = int(warning["iParagraph"]) // 2
                item = pofile.content[item_index]
                start = max(0, int(error["nStart"]) - 40)
                end = max(0, int(error["nEnd"]) + 10)
                word = error["sValue"]
                item.add_warning(
                    self.name,
                    f'Unknown word "{word}" in '
                    f"###{item.msgstr_rst2txt[start:end]}###",
                )

    def filter_out_spelling_error(self, error):
        """Return True when grammalecte error should be ignored."""
        word = error["sValue"]
        if set(word) == {"x"}:
            return True  # word is xxxxx or xxxxxxxx…
        if word.strip() in self.personal_dict:
            return True  # white list
        return False

    def get_personal_dict(self):
        """
        Add spelling white list.

        Based on
        https://raw.githubusercontent.com/python/python-docs-fr/3.8/dict
        """
        download_request = requests.get(
            "https://raw.githubusercontent.com/python/python-docs-fr/3.8/dict"
        )
        download_request.raise_for_status()
        for line in download_request.text.splitlines():
            word = line.strip()
            self.personal_dict.add(word)
            self.personal_dict.add(word.title())
        self.personal_dict.add("HMAC")
        log.error(self.personal_dict)


def install_grammalecte():
    """Install grammalecte CLI."""
    log.warning("Missing grammalecte, trying to install it")
    # with tempfile.TemporaryDirectory(prefix="padpo_") as tmpdirname:
    tmpdirname = "/tmp/_padpo_gramma"  # TODO
    tmpdirname = Path(tmpdirname)
    tmpdirname.mkdir(exist_ok=True)
    download_request = requests.get(
        "https://grammalecte.net/grammalecte/zip/Grammalecte-fr-v1.5.0.zip"
    )
    download_request.raise_for_status()
    zip_file = tmpdirname / "Grammalecte-fr-v1.5.0.zip"
    zip_file.write_bytes(download_request.content)
    with ZipFile(zip_file, "r") as zip_obj:
        zip_obj.extractall(tmpdirname / "Grammalecte-fr-v1.5.0")
    subprocess.run(
        ["pip", "install", str(tmpdirname / "Grammalecte-fr-v1.5.0")]
    )
