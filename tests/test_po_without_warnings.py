"""Test known to be good files."""
from pathlib import Path

from padpo.padpo import check_file


def pytest_generate_tests(metafunc):
    """Parametrize tests according to po_without_warnings directory content."""
    if "known_good_po_file" in metafunc.fixturenames:
        # assume using tox (that cd into tests directory)
        files = list(Path("./po_without_warnings").rglob("*.po"))
        files.extend(Path("./tests/po_without_warnings").rglob("*.po"))
        metafunc.parametrize(
            "known_good_po_file", [str(file_path) for file_path in files]
        )


def test_no_error_no_warning(known_good_po_file):
    """Test known to be good files."""
    errors, warnings = check_file(known_good_po_file)
    assert not errors
    assert not warnings
