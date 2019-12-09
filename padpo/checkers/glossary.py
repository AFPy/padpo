"""Checker for glossary usage."""

from padpo.checkers.baseclass import Checker
from padpo.pofile import PoItem


class GlossaryChecker(Checker):
    """Checker for glossary usage."""

    name = "Glossary"

    def check_item(self, item: PoItem):
        """Check an item in a `*.po` file."""
        if not item.msgstr_full_content:
            return  # no warning
        original_content = item.msgid_full_content.lower()
        translated_content = item.msgstr_full_content.lower()
        for word, translations in glossary.items():
            if word.lower() in original_content:
                for translated_word in translations:
                    if translated_word.lower() in translated_content:
                        break
                else:
                    possibilities = '"'
                    possibilities += '", "'.join(translations[:-1])
                    if len(translations) > 1:
                        possibilities += '" or "'
                    possibilities += translations[-1]
                    possibilities += '"'
                    item.add_warning(
                        self.name,
                        f"Found {word} that is not translated in "
                        f"{possibilities} in ###{item.msgstr_full_content}"
                        "###.",
                    )


# https://github.com/python/python-docs-fr/blob/
# 8a8a9f8dda4d7f40863f8b0d28f547d84f016ad3/CONTRIBUTING.rst
glossary = {
    "-like": ["-compatible"],
    "abstract data type": ["type abstrait"],
    "argument": ["argument"],
    "backslash": ["antislash", "*backslash*", "*backslashes*"],
}
