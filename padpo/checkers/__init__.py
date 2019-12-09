"""Checkers list."""
from padpo.checkers.doublespace import DoubleSpaceChecker
from padpo.checkers.empty import EmptyChecker
from padpo.checkers.fuzzy import FuzzyChecker
from padpo.checkers.glossary import GlossaryChecker
from padpo.checkers.grammalecte import GrammalecteChecker
from padpo.checkers.linelength import LineLengthChecker
from padpo.checkers.nbsp import NonBreakableSpaceChecker

checkers = [
    DoubleSpaceChecker(),
    EmptyChecker(),
    FuzzyChecker(),
    GrammalecteChecker(),
    GlossaryChecker(),
    LineLengthChecker(),
    NonBreakableSpaceChecker(),
]
