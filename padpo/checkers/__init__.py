"""Checkers list."""
from padpo.checkers.empty import EmptyChecker
from padpo.checkers.fuzzy import FuzzyChecker
from padpo.checkers.glossary import GlossaryChecker
from padpo.checkers.linelength import LineLengthChecker

checkers = [
    EmptyChecker(),
    FuzzyChecker(),
    GlossaryChecker(),
    LineLengthChecker(),
]
