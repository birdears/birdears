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


## Introduction


### birdears

`birdears` is a software written in Python 3 for ...

### What is musical ear training

It is a method..

### Features

* questions
* load from config file

## Installing

### Installing the dependencies

#### Arch Linux

```
sudo pacman -Syu sox python python-pip
```

### Installing birdears

`pip install --user --upgrade birdears`

#### In-depth installation

## Running

After installing just run:

`birdears --help`

## Modes

### melodic

### harmonic

### dictation

### instrumental

## Loading from preset files

### Pre-made presets

Birdears cointains some pre-made presets in it's `presets/` subdirectory.

The study for beginners is recommended by following the numeric order of those files (000, 001, then 002 etc.) 

#### Pre-made presets description

Maybe these things would go better in the readhedocs documentation.

### Creating new preset files

You can open the files cointained in birdears premade `presets/` folder to have
an ideia on how config files are made; it is simply the command line options
written in a form `toml` standard.


## Contributing

Those who want to contribute to this project can read [CONTRIBUTING.md](CONTRIBUTING.md).

* * *

```
readme should contain

[toc]

* introduction
  * feats

* screenshot(s)

* installing
  * dependencies
  * pip
    * what is pip
    * installing via pip
    * using a virtualenv
  * cloning the repository

* running

* modes
  * melodic
    * description
    * cli options (--help)
  * harmonic
    * description
    * cli options (--help)
  * dictation
    * description
    * cli options (--help)
  * instrumenetal
    * description
    * cli options (--help)

* loading from config file
  * presets

* * *

* development info
  as is in readme
  c
```
