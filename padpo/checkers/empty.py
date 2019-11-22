"""Checker for missing translations."""


from padpo.checkers.baseclass import Checker
from padpo.pofile import PoItem


class EmptyChecker(Checker):
    """Checker for missing translations."""

    name = "Empty"

    def check_item(self, item: PoItem):
        """Check an item in a `*.po` file."""
        if item.msgid_full_content and not item.msgstr_full_content:
            item.add_warning(self.name, "This entry is not translated yet.")
