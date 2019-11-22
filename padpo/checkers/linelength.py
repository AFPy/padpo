"""Checker for line length."""

from padpo.checkers.baseclass import Checker
from padpo.pofile import PoItem

MAX_LINE_LENGTH = 79


class LineLengthChecker(Checker):
    """Checker for line length."""

    name = "Line length"

    def check_item(self, item: PoItem):
        """Check an item in a `*.po` file."""
        for line in item.msgstr:
            if len(line) > MAX_LINE_LENGTH - 2:  # 2 is for ""
                item.add_error(
                    self.name,
                    f"Line too long ({len(line) + 2} > "
                    f"{MAX_LINE_LENGTH}): {line}",
                )
