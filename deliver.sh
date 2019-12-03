#!/bin/bash

# configuration management
git pull
cat pyproject.toml | grep version
echo "ready?"
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

# tests
tox
echo "ready to publish to PyPI?"
read BOOL

# package creation
poetry build
poetry publish
