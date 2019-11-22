"""Checker for fuzzy translations."""

from padpo.checkers.baseclass import Checker
from padpo.pofile import PoItem


class FuzzyChecker(Checker):
    """Checker for fuzzy translations."""

    def __init__(self):
        """Initialiser."""
        super().__init__(name="Fuzzy")

    def check_item(self, item: PoItem):
        """Check an item in a `*.po` file."""
        if item.fuzzy:
            item.add_warning(self.name, "This entry is tagged as fuzzy.")
