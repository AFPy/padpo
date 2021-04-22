"""Base class for checkers."""

from abc import ABC, abstractmethod

import simplelogging

from padpo.pofile import PoFile, PoItem

log = simplelogging.get_logger()


class Checker(ABC):
    """Base class for checkers."""

    name = "UnknownChecker"  # name displayed in error messages

    def check_file(self, pofile: PoFile):
        """Check a `*.po` file."""
        if not isinstance(pofile, PoFile):
            log.error("%s is not an instance of PoFile", str(pofile))
        for item in pofile.content:
            self.check_item(item)

    @abstractmethod
    def check_item(self, item: PoItem):
        """Check an item in a `*.po` file."""
        return NotImplementedError

    def add_warning(self, level: str, item: PoItem, text: str, prefix:str=None, match:str=None, suffix:str=None):
        silent_method_names = [self.__getattribute__(name) for name in self.__dir__() if name.startswith('silent_')]
        if any([m(item, text, prefix, match, suffix) for m in silent_method_names if callable(m)]):
                return
        if level == 'warning':
            item.add_warning(self.name, text)
        else:
            item.add_error(self.name, text)




def replace_quotes(match):
    """Replace match with « xxxxxxx »."""
    length = len(match.group(0)) - 4
    return "« " + length * "x" + " »"
