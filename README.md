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

* Code in one file (TM) :+1:
* It works on my machine (TM) :computer:
* Need refactoring (TM) :construction_worker:

## Usage

Using the *activated virtual environment* created during the installation:

For a local input file:

```bash
python padpo.py --input-path a_file.po
```

or for a local input directory:

```bash
python padpo.py --input-path a_directory_containing_po_files
```

or for a pull request in python-docs-fr repository (here pull request #978)

```bash
python padpo.py --python-docs-fr 978
```

or for a pull request in a GitHub repository (here python/python-docs-fr/pull/978)

```bash
python padpo.py --github python/python-docs-fr/pull/978
```

![Screenshot](screenshot.png)

## Installation

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

4. Get grammalecte

   ```bash
   pip install wheel
   wget https://grammalecte.net/grammalecte/zip/Grammalecte-fr-v1.5.0.zip
   unzip  Grammalecte-fr-v1.5.0.zip -d Grammalecte-fr-v1.5.0
   cd Grammalecte-fr-v1.5.0
   pip install .
   ```

## Update on PyPI

* git pull
* activate venv
* change version in `setup.py` and in `padpo.__init__`
* clean
  * `rm -rf build/ dist/ eggs/`
  * TODO make a script for this (and better clean)
* `python setup.py sdist`
* `python setup.py bdist_wheel`
* `twine upload dist/*`
