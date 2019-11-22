"""Checker for double spaces."""

import re

from padpo.checkers.baseclass import Checker
from padpo.pofile import PoItem


class DoubleSpaceChecker(Checker):
    """Checker for double spaces."""

    def __init__(self):
        """Initialiser."""
        super().__init__(name="Double space")

    def check_item(self, item: PoItem):
        """Check an item in a `*.po` file."""
        for match in re.finditer(
            r"(.{0,30})\s\s(.{0,30})", item.msgstr_full_content
        ):
            item.add_warning(
                self.name,
                f"Double spaces detected between ###{match.group(1)}### "
                f"and ###{match.group(2)}###",
            )
