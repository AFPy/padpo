# padpo

Linter for gettext files (*.po)

Created to help the translation of official Python docs in French: https://github.com/python/python-docs-fr

Il faut demander aux traducteurs s'ils n'ont pas de pot quand ils traduisent, maintenant ils ont `padpo`…
:smile: :laughing: :stuck_out_tongue_winking_eye: :joy: (note : il était tard le soir quand j'ai trouvé le nom).

**WORK IN PROGRESS**

## License

BSD 3-clause

Pull request are welcome.

## Trademark

* Tests and debuggers are for those who create some bugs™ :bug: :interrobang:

## Usage

Using the *activated virtual environment* created during the installation:

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

## Installation

### Automatic installation

```bash
pip install padpo
```

### Manual installation

1. Create a virtual environment with Python 3.7 and above

   ```bash
   python3.7 -m venv venv
   ```

2. Activate the virtual environment

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Get grammalecte (normally this is done automatically at first usage)

   ```bash
   pip install wheel
   wget https://grammalecte.net/grammalecte/zip/Grammalecte-fr-v1.5.0.zip
   unzip  Grammalecte-fr-v1.5.0.zip -d Grammalecte-fr-v1.5.0
   cd Grammalecte-fr-v1.5.0
   pip install .
   ```

## Update on PyPI

* git pull
* change version in `pyproject.toml` and in `padpo.__init__`
* clean
  * `rm -rf build/ dist/ eggs/`
  * TODO make a script for this (and better clean)
* `poetry build`
* `poetry publish`
