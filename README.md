# BirdEars

[![Maintenance](https://img.shields.io/maintenance/yes/2017.svg?style=flat)](https://github.com/iacchus/birdears/issues/new?title=Is+birdears+still+maintained&body=Please+file+an+issue+if+the+maintained+button+says+no)
[![Travis Build Status](https://img.shields.io/travis/iacchus/birdears.svg?style=flat&label=build)](https://travis-ci.org/iacchus/birdears)
[![Coveralls](https://img.shields.io/coveralls/iacchus/birdears.svg?style=flat&label=Coveralls)](https://coveralls.io/github/iacchus/birdears)
[![Codecov](https://img.shields.io/codecov/c/github/iacchus/birdears.svg?style=flat&label=Codecov)](https://codecov.io/gh/iacchus/birdears)
[![Code Climate coverage](https://img.shields.io/codeclimate/coverage/github/iacchus/birdears.svg?style=flat&label=Codeclimate)](https://codeclimate.com/github/iacchus/birdears)
[![Code Climate issues](https://img.shields.io/codeclimate/issues/github/iacchus/birdears.svg?style=flat&label=cclimate-issues)](https://codeclimate.com/github/iacchus/birdears/issues)
[![Code Climate gpa](https://img.shields.io/codeclimate/github/iacchus/birdears.svg?style=flat&label=cclimate-GPA)](https://codeclimate.com/github/iacchus/birdears)
[![Gitter](https://img.shields.io/gitter/room/birdears/Lobby.svg?style=flat)](https://gitter.im/birdears/Lobby)

[![GitHub (pre-)release](https://img.shields.io/github/release/iacchus/birdears/all.svg?style=flat)](https://github.com/iacchus/birdears/releases)
[![PyPI Status](https://img.shields.io/pypi/status/birdears.svg?style=flat&label=pypi-status)](https://pypi.python.org/pypi/birdears)
[![PyPI Version](https://img.shields.io/pypi/v/birdears.svg?style=flat)](https://pypi.python.org/pypi/birdears)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/birdears.svg?style=flat)](https://pypi.python.org/pypi/birdears)
[![Waffle.io](https://img.shields.io/waffle/label/iacchus/birdears/in%20progress.svg?style=flat)](https://waffle.io/iacchus/birdears)
[![GitHub issues](https://img.shields.io/github/issues/iacchus/birdears.svg?style=flat&label=gh-issues)](https://github.com/iacchus/birdears/issues)
[![Documentation Status](https://readthedocs.org/projects/birdears/badge/?version=latest)](https://birdears.readthedocs.io/en/latest/?badge=latest)

## Functional Ear Training for Musicians

Birdears uses functional ear training method for ear training. It helps you to recognize melodic and harmonic intervals. It uses python 3 and [sox](http://sox.sourceforge.net/).

More documentation is at [birdears Read The Docs](https://birdears.readthedocs.io)

## Installing


### 1. Install the Dependencies

Install `sox` and `python3` (see [below](https://github.com/iacchus/birdears#installing--dependencies)) and,

#### Optional Dependencies

##### Text-user-interface (TUI)

Python's 'urwid' tui library will be necessary to run the TUI; although it is
not implemented yet.

##### Graphical-User-Interface (GUI)

Python's Kivy and SDL2 are required to run the GUI; it's development already
began and can be acessed with:

`$ birdears kivy`

It is not functional yet.

### 2. a. Via pip

You may want to create a virtualenv before installing via `pip`.

```
pip install birdears
```

Then use the command:

```
birdears
```

### 2. b. Clone the repository

```
git clone https://github.com/iacchus/birdears.git
```

Then run the script with:

```
python3 -m birdears
```

## Keybindings for intervals

**MAJOR keyboard keys** (with *chromatics*)

Key Index for major and chromatic major context


```
  keyboard              would represent

 s d   g h j        IIb  IIIb       Vb VIb  VIIb
z x c v b n m  <-  I   II   III  IV   V   VI   VII
```

*(**SHIFT** key meaning an octave higher)*

**MINOR keyboard keys** (with *chromatics*)

Key index for minor and chromatic minor context

```
   keyboard                 would represent
                           in chromatics in
                            'a' minor context

 s   f g   j k   eg.:      a#   c# d#    f# g#
z x c v b n m    -------  a  b c  d  e  f  g
```

## Screenshot or didn't happen

*(development version)*

![birsears screenshot](https://i.imgur.com/PSZCL2a.png)

### Other keys

| Key                  | What it Does                                            |
|                 ---: | :---                                                    |
| <kbd>q</kbd>         | quit.                                                   |
| <kbd>r</kbd>         | to repeat the tonic/interval.                           |
| <kbd>Backspace</kbd> | In melodic dictation, remove previous entered interval. |

## Installing  Dependencies

Submit your distro's too..

### Arch Linux

```
sudo pacman -S python sox
```

## Contributing

### Coding

We ask for people who wants to contribute for the code to look to the musical side first,

#### Checking code style

We use [pep8](https://pypi.python.org/pypi/pep8) to check code formatting:

```
pep8 birdears --exclude=click
```

### Module Documentation

Our documentation is online at [readthedocs](https://birdears.readthedocs.io).

We are using Sphinx to generate documentation for this module. The sphinx resource
files are in the `docs/sphinx/` directory.

We use Google Style Docstrings to write documentation for the API. Here is
Google's online [Python Style Guide](https://google.github.io/styleguide/pyguide.html)
which has some of the specification or Sphinx Napoleon documentation [online](http://www.sphinx-doc.org/en/stable/ext/napoleon.html)
or in [PDF](https://readthedocs.org/projects/sphinxcontrib-napoleon/downloads/pdf/latest/).
Napoleon is the extension used by Sphinx to render Google Docstrings in the
documentation.

#### Runing apidoc

We want to exclude third-party module `click` when generating automatic documentation for the package:

```
sphinx-apidoc -o docs/sphinx/_apidoc birdears/ birdears/click/
```

### End-user Documentation

We aim to build a method / music theory together with this software, maybe in the
GitHub repo's wiki.

### Writing Tests

We use [pytest](https://docs.pytest.org/en/latest/) to run tests; we use [coverage.py](https://coverage.readthedocs.io) to report code coverage;

```
coverage run --source=birdears --module pytest --verbose tests/
```

We use [coveralls](https://coveralls.io/github/iacchus/birdears) and [Travis CI](https://travis-ci.org/iacchus/birdears).

Out tests are in repo's `tests/` directory. We also have a local repoting in html created by coverage, it should be online at https://iacchus.github.io/birdears/coverage-html.

### Feature requests :gift: and suggestions

You are welcome to use [github issues](https://github.com/iacchus/birdears/issues) or [gitter.im](https://gitter.im/birdears/Lobby) to ask for, or give ideia for new features.

## Other stuff

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
