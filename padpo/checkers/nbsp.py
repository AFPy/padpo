"""Checker for missing non breakable spaces."""

import re

from padpo.checkers.baseclass import Checker, replace_quotes
from padpo.pofile import PoItem


class NonBreakableSpaceChecker(Checker):
    """Checker for missing non breakable spaces."""

    name = "NBSP"
    after_silent_re=re.compile('silent-nbsp-after:`([^`]*)`')


    def silent_nbsp_after(self, item: PoItem, text: str, prefix: str, match: str, suffix: str):
        list_ok = self.after_silent_re.findall(item.entry.tcomment)
        for term in list_ok:
            if term in prefix:
                return True


    def check_item(self, item: PoItem):
        """Check an item in a `*.po` file."""
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
                if prefix[-1] not in ":?!.":
                    self.__add_message_space_before(item, prefix, match, suffix)

    def __add_message(self, item, prefix, match, suffix):
        self.add_warning('error', item,
            "Space should be replaced with a non-breakable space in "
            f'"{match}": between ###{prefix}### and ###{suffix}###', prefix, match, suffix,
        )

    def __add_message_space_before(self, item, prefix, match, suffix):
        self.add_warning('error', item,
            f"There should be a non-breakable space before "
            f'"{match[1:]}": between ###{prefix}{match[0]}### and '
            f"###{match[1:]}{suffix}###", prefix, match, suffix,
        )
