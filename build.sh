#!/usr/bin/env bash

# exit on error
set -e

echo 'starting..'

# run pep8
pep8 birdears --exclude=click,toml

# run tests
coverage run --source=birdears --omit=birdears/click/**,birdears/toml/**,birdears/interfaces/gui/**,birdears/interfaces/urwid/** --module pytest --verbose tests/
coverage html --omit='*birdears/click/*','*birdears/toml/*','*birdears/interfaces/gui/*','*birdears/interfaces/urwid/*' -d docs/coverage-html/

# remove pypi builds
rm -rf birdears.egg-info/
rm -rf build/
rm -rf dist/

# convert readme to rst for pypi
rm README.rst
pandoc --from=markdown --to=rst README.md -o README.rst

# ATTENTION
# sphinx apidoc now should be run only by hand, and with care for it's --force option, only when the api changes, as we will be editing the .rst generated with it by hand
#sphinx-apidoc --force -d 4 --module-first --implicit-namespaces -o docs/sphinx/ birdears/ birdears/click/ birdears/toml/ birdears/interfaces/gui birdears/interfaces/urwid

# build sphinx documentation
cd docs/sphinx/
make clean
make html
make latexpdf

# go back to original directory
cd -

# build pypi packages
python setup.py sdist
python setup.py bdist_wheel

git add .
git commit -a -m 'Commit from build.sh'

echo 'end..'

echo 'Please remember of tagging this before pushing to GitHub for a release (ex: git tag 0.1.2; git push --tags)'

read -p "Do you want to upload it to PyPI? [Yy/n]" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    twine upload dist/birdears*
fi

