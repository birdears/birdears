#!/usr/bin/env bash

# exit on error
set -e

echo 'starting..'

# run pep8
pep8 birdears --exclude=click,toml

# run tests
coverage run --source=birdears --omit=birdears/click/**,birdears/toml/** --module pytest --verbose tests/
coverage html --omit='*birdears/click/*','*birdears/toml/*' -d docs/coverage-html/

# remove pypi builds
rm -rf birdears.egg-info/
rm -rf build/
rm -rf dist/

# convert readme to rst for pypi
pandoc --from=markdown --to=rst README.md -o README.rst

# run sphinx-apidoc
#rm docs/sphinx/birdears.rst 
#rm docs/sphinx/birdears.questions.rst
#rm docs/sphinx/modules.rst
#rm docs/sphinx/birdears.interfaces.rst
sphinx-apidoc --force -d 4 -o docs/sphinx/ birdears/ birdears/click/ birdears/toml/


# build sphinx documentation
cd docs/sphinx/
make clean
make html

# go back to original directory
cd -

# build pypi packages
python setup.py sdist
python setup.py bdist_wheel

echo 'end..'
