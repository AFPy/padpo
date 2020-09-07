"""Checker for grammar errors."""

import re
from typing import Set

import requests
import simplelogging
from pygrammalecte import (
    GrammalecteGrammarMessage,
    GrammalecteMessage,
    GrammalecteSpellingMessage,
    grammalecte_text,
)

from padpo.checkers.baseclass import Checker, replace_quotes
from padpo.pofile import PoFile, PoItem

log = simplelogging.get_logger()


class GrammalecteChecker(Checker):
    """Checker for grammar errors."""

    name = "Grammalecte"

    def __init__(self):
        """Initialiser."""
        super().__init__()
        self.personal_dict: Set[str] = set()
        self.get_personal_dict()

    def check_file(self, pofile: PoFile):
        """Check a `*.po` file."""
        if not isinstance(pofile, PoFile):
            log.error("%s is not an instance of PoFile", str(pofile))
        text = pofile.rst2txt()
        text = re.sub(r"«\s(.*?)\s»", replace_quotes, text)
        warnings = grammalecte_text(text)
        self.manage_warnings(warnings, pofile)

    def check_item(self, item: PoItem):
        """Check an item in a `*.po` file (does nothing)."""
        pass

    def manage_warnings(self, warnings: GrammalecteMessage, pofile: PoFile) -> None:
        """Manage warnings returned by grammalecte."""
        for warning in warnings:
            if self.filter_out_grammar_error(warning) or self.filter_out_spelling_error(
                warning
            ):
                continue
            item_index = warning.line // 2
            item = pofile.content[item_index]
            start = max(0, warning.start - 40)
            end = warning.end + 10
            item.add_warning(
                self.name,
                f"{warning.message} => " f"###{item.msgstr_rst2txt[start:end]}###",
            )

    def filter_out_grammar_error(self, warning: GrammalecteMessage) -> bool:
        """Return True when grammalecte error should be ignored."""
        if not isinstance(warning, GrammalecteGrammarMessage):
            return False
        if warning.rule in (
            "esp_milieu_ligne",  # double space
            "nbsp_avant_deux_points",  # NBSP
            "nbsp_avant_double_ponctuation",  # NBSP
        ):
            return True
        if "typo_guillemets_typographiques_simples" in warning.rule:
            return True  # ignore ' quotes
        if warning.message in (
            "Accord de genre erroné : « ABC » est masculin.",
            "Accord de genre erroné : « PEP » est masculin.",
            "Accord de nombre erroné : « PEP » devrait être au pluriel.",
            "Accord de genre erroné : « une entrée » est féminin, « utilisateur » est masculin.",
        ):
            return True
        if "S’il s’agit d’un impératif" in warning.message:
            if warning.start == 0:
                # ignore imperative conjugation at begining of 1st sentence
                return True
        return False

    def filter_out_spelling_error(self, warning: GrammalecteMessage) -> bool:
        """Return True when grammalecte error should be ignored."""
        if not isinstance(warning, GrammalecteSpellingMessage):
            return False
        if set(warning.word) == {"x"}:
            return True  # word is xxxxx or xxxxxxxx…
        if warning.word.strip() in self.personal_dict:
            return True  # white list
        if warning.word.endswith("_"):
            return True
        return False

    def get_personal_dict(self):
        """
        Add spelling white list.

        Based on
        https://raw.githubusercontent.com/python/python-docs-fr/3.9/dict
        """
        download_request = requests.get(
            "https://raw.githubusercontent.com/python/python-docs-fr/3.9/dict"
        )
        download_request.raise_for_status()
        for line in download_request.text.splitlines():
            word = line.strip()
            self.personal_dict.add(word)
            self.personal_dict.add(word.title())
