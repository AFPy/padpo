# padpo

Linter for gettext files (*.po)

Created to help the translation of official Python docs in French: https://github.com/python/python-docs-fr

**WORK IN PROGRESS**

## License

BSD 3-clause

## Trademark

* Code in one file (TM) :+1:
* It works on my machine (TM) :computer:
* Need refactoring (TM) :construction_worker:

## Usage

Using the activated virtual environment created during the installation:

```bash
python3.7 padpo.py a_file.po
```

or

```bash
python3.7 padpo.py a_directory_containing_po_files
```

## Installation

1. Create a virtual environment
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
   wget https://grammalecte.net/grammalecte/zip/Grammalecte-fr-v1.5.0.zip
   unzip  Grammalecte-fr-v1.5.0.zip
   cd Grammalecte-fr-v1.5.0
   pip install .
   ```