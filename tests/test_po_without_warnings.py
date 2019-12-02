from pathlib import Path

from padpo.padpo import check_file


def pytest_generate_tests(metafunc):
    if "known_good_po_file" in metafunc.fixturenames:
        # assume using tox (that cd into tests directory)
        directory = Path("./po_without_warnings")
        files = directory.rglob("*.po")
        metafunc.parametrize(
            "known_good_po_file", [str(file) for file in files]
        )


def test_coverage(known_good_po_file):
    # TODO get an empty list of warnings
    assert check_file(known_good_po_file) == False
