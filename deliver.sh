#!/bin/bash

git pull
cat padpo/__init__.py | grep version
cat setup.py | grep version
echo "ready ?"
read BOOL

source venv/bin/activate

# clean
rm -rf build/ dist/ .eggs/
find . -name '*.egg-info' -exec rm -fr {} +
find . -name '*.egg' -exec rm -fr {} +
find . -name '*.pyc' -exec rm -f {} +
find . -name '*.pyo' -exec rm -f {} +
find . -name '*~' -exec rm -f {} +
find . -name '__pycache__' -exec rm -fr {} +
rm -fr .tox/
rm -f .coverage
rm -fr htmlcov/
rm -fr .pytest_cache


# package creation
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
