"""Checker for glossary usage."""

import re

from padpo.checkers.baseclass import Checker
from padpo.pofile import PoItem


class GlossaryChecker(Checker):
    """Checker for glossary usage."""

    name = "Glossary"

    def check_item(self, item: PoItem):
        """Check an item in a `*.po` file."""
        if not item.msgstr_full_content:
            return  # no warning
        original_content = item.msgid_rst2txt.lower()
        original_content = re.sub(r"« .*? »", "", original_content)
        translated_content = item.msgstr_full_content.lower()
        for word, translations in glossary.items():
            if re.match(fr"\b{word.lower()}\b", original_content):
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
                        f'Found "{word}" that is not translated in '
                        f"{possibilities} in ###{item.msgstr_full_content}"
                        "###.",
                    )


# https://github.com/python/python-docs-fr/blob/
# 8a8a9f8dda4d7f40863f8b0d28f547d84f016ad3/CONTRIBUTING.rst
glossary = {
    "-like": ["-compatible"],
    "abstract data type": ["type abstrait"],
    "abstract data types": ["types abstraits"],
    "argument": ["argument"],
    "arguments": ["arguments"],
    "backslash": ["antislash", "*backslash*"],
    "backslashes": ["antislashs", "*backslashes*"],
    "backtrace": ["trace d'appels", "trace de pile"],
    "backtraces": ["traces d'appels", "traces de pile"],
    "big-endian": ["gros-boutiste"],
    "bound": ["lié"],
    "bug": ["bogue", "*bug*"],
    "bugs": ["bogues", "*bugs*"],
    "built-in": ["native"],
    "built-ins": ["fonctions natives"],
    "callback": ["fonction de rappel"],
    "callbacks": ["fonctions de rappel"],
    "call stack": ["pile d'appels"],
    "call stacks": ["piles d'appels"],
    "debugging": ["débogage"],
    "deep copy": ["copie récursive", "copie profonde"],
    "double quote": ["guillemet"],
    "double quotes": ["guillemets"],
    "deprecated": ["obsolète"],
    "e.g.": ["p. ex.", "par exemple"],
    "et al.": ["et autre", "et ailleurs"],
    "export": ["exporter", "exportation"],
    "exports": ["exportations"],
    "expression": ["expression"],
    "expressions": ["expressions"],
    "garbage collector": ["ramasse-miettes"],
    "getter": ["accesseur"],
    "getters": ["accesseurs"],
    "i.e": ["c.-à-d.", "c'est-à-dire"],
    "identifier": ["identifiant"],
    "identifiers": ["identifiants"],
    "immutable": ["immuable"],
    "import": ["importer", "importation"],
    "imports": ["importations"],
    "installer": ["installateur"],
    "installers": ["installateurs"],
    "interpreter": ["interpréteur"],
    "interpreters": ["interpréteurs"],
    "library": ["bibliothèque"],
    "libraries": ["bibliothèques"],
    "list comprehension": ["liste en compréhension"],
    "list comprehensions": ["listes en compréhension"],
    "little-endian": ["petit-boutiste"],
    "mixin type": ["type de mélange"],
    "mixin types": ["types de mélange"],
    "mutable": ["muable"],
    "namespace": ["espace de nommage", "espace de noms"],
    "namespaces": ["espaces de nommage", "espaces de noms"],
    "parameter": ["paramètre"],
    "parameters": ["paramètres"],
    "pickle": ["sérialiser"],
    "prompt": ["invite"],
    "raise": ["lever"],
    "raised": ["levé"],
    "regular expression": ["expression rationnelle", "expression régulière"],
    "regular expressions": [
        "expressions rationnelles",
        "expressions régulières",
    ],
    "return": ["renvoie"],
    "returns": ["renvoie"],
    "returned": ["renvoyé"],
    "setter": ["mutateur"],
    "setters": ["mutateurs"],
    "simple quote": ["guillemet simple"],
    "simple quotes": ["guillemets simples"],
    "socket": ["connecteur", "interface de connexion"],
    "sockets": ["connecteurs", "interfaces de connexion"],
    "statement": ["instruction"],
    "statements": ["instructions"],
    "subprocess": ["sous-processus"],
    "subprocesses": ["sous-processus"],
    "thread": ["fil d'exécution"],
    "threads": ["fils d'exécution"],
    "traceback": ["trace d'appels", "trace de pile"],
    "tracebacks": ["traces d'appels", "traces de pile"],
    "underscore": ["tiret bas", "*underscore*"],
    "underscores": ["tirets bas", "*underscores*"],
    "whitespace": ["caractère d'espacement"],
    "whitespaces": ["caractères d'espacement"],
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
        "generator": ["générateur", "génératrice"],
        "generator iterator": [
            "itérateur de générateur",
            "iterateurs de générateur",
        ],
        "generator expression": [
            "expression génératrice",
            "expressions génératrices",
        ],
        "generic function": ["fonction générique", "fonctions génériques"],
        "GIL": ["GIL"],
        "global interpreter lock": ["verrou global de l'interpréteur"],
        "hash-based pyc": ["*pyc* utilisant le hachage"],
        "hashable": ["hachable"],
        # "IDLE": ["IDLE"],  # confusion with "idle"
        "immutable": ["immuable"],
        "import path": ["chemin des importations", "chemins des importations"],
        "importing": ["importer", "important", "importation"],
        "importer": ["importateur"],
        "interactive": ["interactif"],
        "interpreted": ["interprété"],
        "interpreter shutdown": ["arrêt de l'interpréteur"],
        "iterable": ["itérable"],
        "iterator": ["itérateur"],
        "key function": ["fonction clé"],
        "keyword argument": ["argument nommé", "arguments nommés"],
        "lambda": ["lambda"],
        "list": ["*list*", "liste"],
        "list comprehension": ["liste en compréhension", "liste en intension"],
        "loader": ["chargeur"],
        "magic method": ["méthode magique", "méthodes magiques"],
        "mapping": ["tableau de correspondance", "tableaux de correspondance"],
        "meta path finder": ["chercheur dans les méta-chemins"],
        "metaclass": ["métaclasse"],
        "method": ["méthode"],
        "method resolution order": ["ordre de résolution des méthodes"],
        "module": ["module"],
        "module spec": ["spécificateur de module"],
        "MRO": ["MRO"],
        "mutable": ["muable"],
        "named tuple": ["n-uplet nommé", "n-uplets nommés"],
        "namespace": [
            "espace de nommage",
            "espace de noms",
            "espaces de nommage",
            "espaces de noms",
        ],
        "namespace package": ["paquet-espace de nommage"],
        "nested scope": ["portée imbriquée", "portées imbriquées"],
        "new-style class": ["nouvelle classe", "nouvelles classes"],
        "object": ["objet"],
        "package": ["paquet"],
        "parameter": ["paramètre"],
        "path entry": ["entrée de chemin"],
        "path entries": ["entrées de chemin"],
        "path entry finder": ["chercheur de chemins"],
        "path entry hook": ["point d'entrée pour la recherche dans *path*"],
        "path based finder": ["chercheur basé sur les chemins"],
        "path-like object": ["objet simili-chemin"],
        "PEP": ["PEP"],
        "portion": ["portion"],
        "positional argument": [
            "argument positionnel",
            "arguments positionnels",
        ],
        "provisional API": ["API provisoire"],
        "provisional package": ["paquet provisoire", "paquets provisoires"],
        "pythonic": ["*pythonique*"],
        "qualified name": ["nom qualifié", "noms qualifiés"],
        "reference count": ["nombre de références"],
        "regular package": ["paquet classique", "paquets classiques"],
        "__slots__": ["``__slots__``"],
        "sequence": ["séquence"],
        "single dispatch": ["distribution simple"],
        "slice": ["tranche"],
        "special method": ["méthode spéciale", "méthodes spéciales"],
        "statement": ["instruction"],
        "text encoding": ["encodage de texte"],
        "text file": ["fichier texte", "fichiers texte"],
        "triple quoted string": [
            "chaîne entre triple guillemets",
            "chaînes entre triple guillemets",
        ],
        "type": ["type"],
        "type alias": ["alias de type"],
        "type hint": ["indication de type", "indications de type"],
        "universal newlines": ["retours à la ligne universels"],
        "variable annotation": [
            "annotation de variable",
            "annotations de variables",
        ],
        "virtual environment": [
            "environnement virtuel",
            "environnements virtuels",
        ],
        "virtual machine": ["machine virtuelle", "machines virtuelles"],
        "zen of Python": ["le zen de Python"],
    }
)

