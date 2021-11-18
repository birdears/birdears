# CONTRIBUTING

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [CONTRIBUTING](#contributing)
	- [Coding](#coding)
		- [Checking code style](#checking-code-style)
	- [Module Documentation](#module-documentation)
		- [Runing apidoc](#runing-apidoc)
	- [End-user Documentation](#end-user-documentation)
	- [Writing Tests](#writing-tests)
	- [Feature requests :gift: and suggestions](#feature-requests-gift-and-suggestions)
- [Other stuff](#other-stuff)

<!-- /TOC -->

## Coding

We ask for people who wants to contribute for the code to look to the musical side first,

### Checking code style

We use [pep8](https://pypi.python.org/pypi/pep8) to check code formatting:

```
pep8 birdears --exclude=click
```

## Module Documentation

Our documentation is online at [readthedocs](https://birdears.readthedocs.io).

We are using Sphinx to generate documentation for this module. The sphinx resource
files are in the `docs/sphinx/` directory.

We use Google Style Docstrings to write documentation for the API. Here is
Google's online [Python Style Guide](https://google.github.io/styleguide/pyguide.html)
which has some of the specification or Sphinx Napoleon documentation [online](http://www.sphinx-doc.org/en/stable/ext/napoleon.html)
or in [PDF](https://readthedocs.org/projects/sphinxcontrib-napoleon/downloads/pdf/latest/).
Napoleon is the extension used by Sphinx to render Google Docstrings in the
documentation. Here is [a good documentation on Google-style Docstrings.](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html).

### Runing apidoc

We want to exclude third-party module `click` when generating automatic documentation for the package:

```
sphinx-apidoc -o docs/sphinx/_apidoc birdears/ birdears/click/
```

### Sphinx reStructuredText references

* http://www.sphinx-doc.org/en/stable/rest.html
* http://docutils.sourceforge.net/docs/user/rst/quickref.html
* https://docs.python.org/devguide/documenting.html#style-guide

### Section Conventions

As in https://docs.python.org/devguide/documenting.html#sections:

#### 7.3.6. Sections

Section headers are created by underlining (and optionally overlining) the section title with a punctuation character, at least as long as the text:

```
=================
This is a heading
=================
```

Normally, there are no heading levels assigned to certain characters as the structure is determined from the succession of headings. However, for the Python documentation, here is a suggested convention:

* # with overline, for parts
* * with overline, for chapters
* =, for sections
* -, for subsections
* ^, for subsubsections
* ", for paragraphs

## End-user Documentation

We aim to build a method / music theory together with this software, maybe in the
GitHub repo's wiki.

## Writing Tests

We use [pytest](https://docs.pytest.org/en/latest/) to run tests; we use [coverage.py](https://coverage.readthedocs.io) to report code coverage;

```
coverage run --source=birdears --module pytest --verbose tests/
```

We use [coveralls](https://coveralls.io/github/iacchus/birdears) and [Travis CI](https://travis-ci.org/iacchus/birdears).

Out tests are in repo's `tests/` directory. We also have a local repoting in html created by coverage, it should be online at https://iacchus.github.io/birdears/coverage-html.

## Feature requests :gift: and suggestions

You are welcome to use [github issues](https://github.com/iacchus/birdears/issues) or our [matrix chat](https://matrix.to/#/#birdears:mozilla.org) to ask for, or give ideia for new features.

# Other stuff

We are using pandoc to convert README from .md to .rst:

```
pandoc --from=markdown --to=rst README.md -o README.rst
```

To generate package for PyPI:

```
python setup.py sdist
python setup.py bdist_wheel
```

Read also [TODO.md](TODO.md)
