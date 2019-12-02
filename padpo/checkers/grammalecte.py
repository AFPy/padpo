"""Checker for grammar errors."""

import json
import re
import subprocess
import tempfile
from pathlib import Path
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
        Path(filename).unlink()

    def check_item(self, item: PoItem):
        """Check an item in a `*.po` file (does nothing)."""
        pass

    def filter_out(self, error):
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
        return False


def install_grammalecte():
    """Install grammalecte CLI."""
    log.warning("Missing grammalecte, trying to install it")
    # with tempfile.TemporaryDirectory(prefix="padpo_") as tmpdirname:
    tmpdirname = "/tmp/_padpo_gramma"
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
