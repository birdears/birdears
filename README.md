# BirdEars

[![Join the chat at https://gitter.im/birdears/Lobby](https://badges.gitter.im/birdears/Lobby.svg)](https://gitter.im/birdears/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Travis Build Status](https://img.shields.io/travis/iacchus/birdears.svg?label=build)](https://travis-ci.org/iacchus/birdears)
[![Coveralls](https://img.shields.io/coveralls/iacchus/birdears.svg?label=Coveralls)](https://coveralls.io/github/iacchus/birdears)
[![Codecov](https://img.shields.io/codecov/c/github/iacchus/birdears.svg?label=Codecov)](https://codecov.io/gh/iacchus/birdears)
[![Code Climate coverage](https://img.shields.io/codeclimate/coverage/github/iacchus/birdears.svg?label=Codeclimate)](https://codeclimate.com/github/iacchus/birdears)
[![Code Climate issues](https://img.shields.io/codeclimate/issues/github/iacchus/birdears.svg?label=issues)](https://codeclimate.com/github/iacchus/birdears/issues)
[![Code Climate gpa](https://img.shields.io/codeclimate/github/iacchus/birdears.svg?label=GPA)]()

## Functional Ear Training for Musicians

In current development though functional

## Usage

### 1. Install the Dependencies

Install `sox` and `python3` (see [below](https://github.com/iacchus/birdears#installing--dependencies)) and,

### 2. clone the repository

```
git clone https://github.com/iacchus/birdears.git
```

### 3. and just run the script:

```
python3 birdears.py
```

#### or

```
chmod +x birdears.py
./birdears.py
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

| Key          | What it Does                  |
|         ---: | :---                          |
| <kbd>q</kbd> | quit.                         |
| <kbd>r</kbd> | to repeat the tonic/interval. |

## Installing  Dependencies

Submit your distro's too..

### Arch Linux

```
sudo pacman -S python sox
```

## Contributing

### Documentation

We are beginning to use [numpydoc](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt)
to document the library.

Also see `pdoc --html`

### Writing Tests

We use [pytest](https://docs.pytest.org/en/latest/) to run tests; we use [coverage.py](https://coverage.readthedocs.io) to report code coverage;

```
coverage run --source=birdears --module pytest --verbose tests/
```

We use [coveralls](https://coveralls.io/github/iacchus/birdears) and [Travis CI](https://travis-ci.org/iacchus/birdears).

Out tests are in repo's `tests/` directory.

### Etc

We aim to build a method / music theory together with this software, maybe in the
GitHub repo's wiki.

### Misc documentation

[PEP 8](https://pep8.org) — the Style Guide for Python Code

[Python.org PEP8](https://www.python.org/dev/peps/pep-0008/)
