# padpo

[![PyPI](https://img.shields.io/pypi/v/padpo.svg)](https://pypi.python.org/pypi/padpo)
[![PyPI](https://img.shields.io/pypi/l/padpo.svg)](https://github.com/vpoulailleau/padpo/blob/master/LICENSE)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Downloads](https://pepy.tech/badge/padpo)](https://pepy.tech/project/padpo)
[![Tests](https://github.com/AFPy/padpo/workflows/Tests/badge.svg)](https://github.com/AFPy/padpo/actions?query=workflow%3ATests)
[![Maintainability](https://api.codeclimate.com/v1/badges/bbd3044291527d667778/maintainability)](https://codeclimate.com/github/AFPy/padpo/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/bbd3044291527d667778/test_coverage)](https://codeclimate.com/github/AFPy/padpo/test_coverage)

Linter for gettext files (\*.po)

Created to help the translation of official Python docs in French: https://github.com/python/python-docs-fr

Il faut demander aux traducteurs s'ils n'ont pas de pot quand ils traduisent, maintenant ils ont `padpo`…
:smile: :laughing: :stuck_out_tongue_winking_eye: :joy: (note : il était tard le soir quand j'ai trouvé le nom).

## License

BSD 3-clause

Pull request are welcome.

## Padpo is part of poutils!

[Poutils](https://pypi.org/project/poutils) (`.po` utils) is a metapackage to easily install useful Python tools to use with po files
and `padpo` is a part of it! Go check out [Poutils](https://pypi.org/project/poutils) to discover the other tools!

## Usage

Using the _activated virtual environment_ created during the installation:

For a local input file:

```bash
padpo --input-path a_file.po
```

or for a local input directory:

```bash
padpo --input-path a_directory_containing_po_files
```

or for a pull request in python-docs-fr repository (here pull request #978)

```bash
padpo --python-docs-fr 978
```

or for a pull request in a GitHub repository (here python/python-docs-fr/pull/978)

```bash
padpo --github python/python-docs-fr/pull/978
```

![Screenshot](screenshot.png)

### Color

By default, the output is colorless, and formatted like GCC messages. You can use `-c`
or `--color` option to get a colored output.

## Installation

### Automatic installation

```bash
pip install padpo
```

## Update on PyPI

`./deliver.sh`

## Changelog

### v0.12.0 (2024-11-06)

- use `uv`
- use `pygrammalecte` v1.4.0
- compatible with Python 3.9 to 3.13

### v0.11.0 (2021-02-02)

- update glossary (fix #58)

### v0.10.0 (2020-12-04)

- use `pygrammalecte` v1.3.0
- use GitHub Actions

### v0.9.0 (2020-09-07)

- use `pygrammalecte` default message for spelling errors

### v0.8.0 (2020-08-25)

- use [`pygrammalecte`](https://github.com/vpoulailleau/pygrammalecte)
- add continuous integration
- fix #12, #13, #14, #15, #17, #18, #20
- add `--color` CLI option to get a colored output (default is colorless)

### v0.7.0 (2019-12-11)

- add `--version` CLI option to display the current version of `padpo`
- `--input-path` CLI option now accepts several paths as in
  `padpo --input-path file1.po file2.po directory1 directory2` or
  `padpo -i file1.po file2.po directory1 directory2`

### v0.6.0 (2019-12-9)

- check errors against defined glossaries

### v0.5.0 (2019-12-3)

- check spelling errors with grammalecte
- tag releases!

### v0.4.0 (2019-12-2)

- use poetry: https://poetry.eustace.io/docs/
- add some tests with tox and pytests
- fix some false positive issues with grammalecte
