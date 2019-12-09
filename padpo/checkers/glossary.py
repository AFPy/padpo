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
    "backtrace": [
        "trace d'appels",
        "trace de pile",
        "traces d'appels",
        "traces de pile",
    ],
    "big-endian": ["gros-boutiste"],
    "bound": ["lié"],
    "bug": ["bogue", "*bug*", "*bugs*"],
    "built-in": ["native"],
    "callback": ["fonction de rappel", "fonctions de rappel"],
    "call stack": ["pile d'appels"],
    "debugging": ["débogage"],
    "deep copy": ["copie récursive", "copie profonde"],
    "double quote": ["guillemet"],
    "deprecated": ["obsolète"],
    "e.g.": ["p. ex.", "par exemple"],
    "et al.": ["et autre", "et ailleurs"],
    "export": ["exporter", "exportation"],
    "expression": ["expression"],
    "garbage collector": ["ramasse-miettes"],
    "getter": ["accesseur"],
    "i.e": ["c.-à-d.", "c'est-à-dire"],
    "identifier": ["identifiant"],
    "immutable": ["immuable"],
    "import": ["importer", "importation"],
    "installer": ["installateur"],
    "interpreter": ["interpréteur"],
    "library": ["bibliothèque"],
    "libraries": ["bibliothèques"],
    "list comprehension": ["liste en compréhension"],
    "little-endian": ["petit-boutiste"],
    "mixin type": ["type de mélange"],
    "mutable": ["muable"],
    "namespace": [
        "espace de nommage",
        "espace de noms",
        "espaces de nommage",
        "espaces de noms",
    ],
    "parameter": ["paramètre"],
    "pickle": ["sérialiser"],  # TODO word boundaries (regex ?)
    "prompt": ["invite"],
    "raise": ["lever", "levé"],
    "regular expression": [
        "expression rationnelle",
        "expressions rationnelles",
        "expression régulière",
        "expressions régulières",
    ],
    "return": ["renvoie", "renvoyé"],
    "setter": ["mutateur"],
    "simple quote": ["guillemet simple", "guillemets simples"],
    "socket": [
        "connecteur",
        "interface de connexion",
        "interfaces de connexion",
    ],
    "statement": ["instruction"],
    "subprocess": ["sous-processus"],
    "thread": ["fil d'exécution", "fils d'exécution"],
    "traceback": [
        "trace d'appels",
        "trace de pile",
        "traces d'appels",
        "traces de pile",
    ],
    "underscore": ["tiret bas", "*underscore*"],
    "whitespace": ["caractère d'espacement", "caractères d'espacement"],
}

# https://github.com/python/python-docs-fr/blob/
# ccc2e5863e8d814c3ec9463be70db6bbaf611462/glossary.po
glossary.update(
    {
        "abstract base class": [
            "classe de base abstraite",
            "classes de base abstraites",
        ],
        "annotation": ["annotation"],
        "asynchronous context manager": [
            "gestionnaire de contexte asynchrone",
            "gestionnaires de contexte asynchrone",
        ],
        "asynchronous generator": [
            "générateur asynchrone",
            "générateurs asynchrones",
        ],
        "asynchronous iterable": [
            "itérable asynchrone",
            "itérables asynchrones",
        ],
        "asynchronous": ["asynchrone"],
        "attribute": ["attribut"],
        "awaitable": ["*awaitable*"],
        "BDFL": ["*BDFL*"],
        "binary file": ["fichier binaire", "fichiers binaires"],
        "bytes-like object": [
            "objet octet-compatible",
            "objets octet-compatible",
        ],
        "bytecode": ["code intermédiaire", "*bytecode*"],
        "class": ["classe"],
        "class variable": ["variable de classe", "variables de classe"],
        "coercion": ["coercition"],
        "complex number": ["nombre complexe", "nombres complexes"],
        "context manager": [
            "gestionnaire de contexte",
            "gestionnaires de contexte",
        ],
        "context variable": ["variable de contexte", "variables de contexte"],
        "contiguous": ["contigu"],
        "coroutine": ["coroutine"],
        "CPython": ["CPython"],
        "decorator": ["décorateur"],
        "descriptor": ["descripteur"],
        "dictionary": ["dictionnaire"],
        "dictionary view": ["vue de dictionnaire", "vues de dictionnaire"],
        "docstring": [
            "*docstring*",
            "*docstrings*",
            "chaîne de documentation",
            "chaînes de documentation",
        ],
        "duck-typing": ["*duck-typing*"],
        "expression": ["expression"],
        "extension module": ["module d'extension", "modules d'extension"],
        "f-string": ["f-string"],
        "file object": ["objet fichier", "objets fichier"],
        "file-like object": [
            "objet fichier-compatible",
            "objets fichier-compatible",
        ],
        "finder": ["chercheur"],
        "floor division": ["division entière", "divisions entières"],
        "function": ["fonction"],
        "function annotation": [
            "annotation de fonction",
            "annotations de fonction",
        ],
        "__future__": ["__future__"],
        "garbage collection": ["ramasse-miettes"],
        "generator": ["générateur"],
        "iterator": ["itérateur"],
    }
)

