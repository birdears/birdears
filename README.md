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

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [BirdEars](#birdears)
	- [Functional Ear Training for Musicians](#functional-ear-training-for-musicians)
	- [Installing](#installing)
		- [1. Install the Dependencies](#1-install-the-dependencies)
			- [Optional Dependencies](#optional-dependencies)
				- [Text-user-interface (TUI)](#text-user-interface-tui)
				- [Graphical-User-Interface (GUI)](#graphical-user-interface-gui)
		- [2. a. Via pip](#2-a-via-pip)
		- [2. b. Clone the repository](#2-b-clone-the-repository)
	- [Keybindings for intervals](#keybindings-for-intervals)
	- [Screenshot or didn't happen](#screenshot-or-didnt-happen)
		- [Other keys](#other-keys)
	- [Installing  Dependencies](#installing-dependencies)
		- [Arch Linux](#arch-linux)
	- [Contributing](#contributing)

<!-- /TOC -->

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
pip install --upgrade birdears
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

**readme should be rewritten**

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

![birdears screenshot](https://i.imgur.com/PSZCL2a.png)

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

Those who want to contribute to this project can read [CONTRIBUTING.md](CONTRIBUTING.md).
