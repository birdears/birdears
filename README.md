# birdears

[![Maintenance](https://img.shields.io/maintenance/yes/2021.svg?style=flat-square)](https://github.com/iacchus/birdears/issues/new?title=Is+birdears+still+maintained&body=Please+file+an+issue+if+the+maintained+button+says+no)
[![Travis Build Status](https://img.shields.io/travis/iacchus/birdears.svg?style=flat-square&label=build)](https://travis-ci.org/iacchus/birdears)
[![Coveralls](https://img.shields.io/coveralls/iacchus/birdears.svg?style=flat-square&label=coverage)](https://coveralls.io/github/iacchus/birdears)
[![Awesome Sheet Music](https://img.shields.io/badge/awesome-sheet%20music-blue.svg?style=flat-square&logoWidth=14;&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA%2FwD%2FAP%2BgvaeTAAAACXBIWXMAAD2EAAA9hAHVrK90AAAAB3RJTUUH4QYVEQ4dGSq4mgAAAuVJREFUKM8FwUtoHGUAB%2FD%2F983s7CSb7s6%2BsrtJtqbEJA21llgQi4VaCL5QRKXQg6JXEUTqrfQi9CTozYPeUgrtxceh1kbEEEtBeslzTbdrup109r2zMzvZ2Xl8s9%2F4%2B5Hvfg4vOGpzqJf3aCpY%2FfTMi5OvE%2B6mdx%2Fud0YjP5PNxpiuh6X9%2F3I%2F6mzcScvT%2BvjYCUucknhkYSnvNYTvr5169YNLCEMAHKfPvZxwrBZaqoaGWn%2BNBNWlJ4dzn3147n2totckelwZhdr%2B9U%2FOvnnx0kRSgTJdhOBpIPYzSMyE7DaQJEcoFOO5lFK%2BeszcjxblGU%2BUzHosO5%2B6Ek2kQUYuupt3cXxxEoTIYN0WFDGHNnGwvVFGLJ1eXqv%2B8dzJPK%2FRhvbLKwtnzoI7BvyBjqBzCGEiC5ougAgCCJUAymHZPuYWc8J27cGV3c76jOgM9FlwjpE7APMZAscHH%2FYQsBgAhqBvYCyeREgRbm%2FV3aXixLwf6DFxqpCIDpqPQMQIjNoTBLaN9uYO7v30T9h72sHlL1fIV1%2Bvh0mBsp16na6czmUuJM5XaM%2Fo5UEp9JqGeGEO7tBHfGYW73x8kay8%2FTwRvADL02PIClw6shkxbd8sxl%2Fo0yghVl%2FvIyoL0DY30G8ZcKt7kDnDVDGHQbOFNAFZzlC4ozDiub6SofGAWsNIZWh10X7WwtODNsyeh15ZhfVYw6M%2Ft9Do%2B1jdMsPAC%2BEEHCyAy5WCT5VE%2FqDyr4rh0IZlu%2BygZg%2FdaAw2O0KTUWh%2FVXBe4kT1KVgIeAPh1rHxJBdufHsnKJXvXK7slIV61SodNI7iswVRDgnB%2FEuz8IiDvs1xs2yH1Q099oaZfyj5lkRVf4Ta4%2B69vuF6ajeodkRJ2tzroVRq4%2F5v2xiTFahd115ITn5eu23L5on3mBn5O0UNTxB2m%2FIDdZD5hiUW7qcyhd%2B%2F%2BHUNc2%2B9i8OBwFfXDo11Hfjho2t3I4tRIRoYNBAV738fRoHSSCa2GwAAAABJRU5ErkJggg%3D%3D)](https://iacchus.github.io/awesome-sheet-music/)

[![GitHub (pre-)release](https://img.shields.io/github/release/iacchus/birdears/all.svg?style=flat-square)](https://github.com/iacchus/birdears/releases)
[![PyPI Status](https://img.shields.io/pypi/status/birdears.svg?style=flat-square&label=pypi-status)](https://pypi.python.org/pypi/birdears)
[![PyPI Version](https://img.shields.io/pypi/v/birdears.svg?style=flat-square)](https://pypi.python.org/pypi/birdears)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/birdears.svg?style=flat-square)](https://pypi.python.org/pypi/birdears)
[![Documentation Status](https://img.shields.io/badge/readthedocs-latest-orange.svg?style=flat-square)](https://birdears.readthedocs.io/en/latest/)

| **Licensed with [GNU AGPLv3](https://github.com/iacchus/birdears/blob/master/LICENSE)** |
| ----------------- |
| [![agpl3](https://github.com/iacchus/birdears/raw/master/agplv3-155x51.png)](https://github.com/iacchus/birdears/blob/master/LICENSE) |

<!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Introduction](#introduction)
	- [birdears](#birdears)
	- [What is musical ear training](#what-is-musical-ear-training)
	- [Features](#features)
- [Installing](#installing)
	- [Installing the dependencies](#installing-the-dependencies)
		- [Arch Linux](#arch-linux)
	- [Installing birdears](#installing-birdears)
		- [In-depth installation](#in-depth-installation)
		- [Alternative installation: Cloning this Repository](#alternative-installation-cloning-this-repository)
- [Running](#running)
- [Keybindings](#keybindings)
- [Documentation](#documentation)
- [Contributing](#contributing)

<!-- /TOC -->

### Support Channels


| Channel | Site | Description |
| --- | --- | --- |
| **Chat (Matrix)** | [#birdears:mozilla.org](https://matrix.to/#/#birdears:mozilla.org) | *chat channel* |
| **GitHub Discussions** | [discussions](https://github.com/iacchus/birdears/discussions) | *general discussion* |
| **GitHub Issues** | [issues](https://github.com/iacchus/birdears/issues) | *for issues with the software* |
| **Documentation** | [https://birdears.readthedocs.io/](https://birdears.readthedocs.io/) |  *extended documentation at **ReadTheDocs*** |
| **PyPI** | [https://pypi.python.org/pypi/birdears](https://pypi.python.org/pypi/birdears) | *python package/repository* |
| **GitHub** | [https://github.com/iacchus/birdears](https://github.com/iacchus/birdears) | *mainline repository* |

### TUI

![screenshot](https://github.com/iacchus/birdears/raw/master/screen-20190211-163428-BRT.png)

### CLI

![birdears screencast](https://github.com/iacchus/birdears/raw/master/use.gif)

## Introduction

### birdears

`birdears` is a software written in Python 3 for ear training for musicians
(musical intelligence, transcribing music, composing). It is a clone of the
method used by [Funcitional Ear Trainer](https://play.google.com/store/apps/details?id=com.kaizen9.fet.android) app for Android.

It comes with four modes, or four kind of exercises, which are: `melodic`, `harmonic`, `dictation` and `instrumental`.

In resume, with the *melodic* mode two notes are played one after the other and you have to guess the interval; with the
`harmonic` mode, two notes are played simoutaneously (harmonically) and you should guess the interval.

With the *dictation* mode, more than 2 notes are played (*ie*., a melodic dictation) and you should tell what are the intervals
between them.

With the *instrumental* mode, it is a like the *dictation*, but you will be expected to play the notes on your instrument, *ie*.,
birdears will not wait for a typed reply and you should prectice with your own judgement. The melody can be repeat any times and
you can have as much time as you want to try it out.

### What is musical ear training

*this needs to be written. The method.*

It is currently [being written here](WRITE-ME-method.md)

### Features

* Different kind of exercises for ear training.
* Pretty much configurable: you can create more difficult exercises as you progress.
* Exercises from configuration files: you can make presets and share them:
* you can make your own presets
* Can be used interactively from a Python console. *(docs needed)*
* Can be used as a Python library. *(docs needed)*

## Installing

### Installing the dependencies

`birdears` depends only on `python >= 3.5` and `sox` (which should be installed by your distribution's package manager,
supposing you're using linux, and which provides the `play` command.) 

#### Arch Linux

```
sudo pacman -Syu sox python python-pip
```

### Installing birdears

`pip3 install --user --upgrade --no-cache-dir birdears`

#### In-depth installation

You can choose to use a virtualenv to use birdears; this should give you an idea on how to setup one virtualenv.

You should first install virtualenv (for python3) using your distribution's package (supposing you're on linux),
then on terminal:

```
virtualenv -p python3 ~/.venv # use the directory ~/.venv/ for the virtualenv

source ~/.venv/bin/activate   # activate the virtualenv; this should be done
                              # every time you may want to run the software
                              # installed here.

pip3 install birdears         # this will install the software

birdears --help               # and this will run it
```

#### Alternative installation: Cloning this Repository

This way you can have the mainline version of `birdears`, which sometimes takes time to be updated to `pip`.

1. Install `python3` and `sox` for your linux distribution.

2. Clone the repository:

*ex. cloning it ro a directory named `birdears-root`*

```
git clone https://github.com/iacchus/birdears.git birdears-root
```

3. Set the `PYTHONPATH` environment variable to the directory you cloned `birdears`

*first example:*

```
export PYTHONPATH='/home/YOUR_USERNAME/my-git-repos/birdears-root'
python -m birdears
```

*second example:*

```
PYTHONPATH='/home/YOUR_USERNAME/my-git-repos/birdears-root' python -m birdears
```

**tip:**

You can also add an *alias* to your `.bashrc` to simplify this

```
alias birdears="PYTHONPATH='/home/YOUR_USERNAME/my-git-repos/birdears-root' python -m birdears"
```

**explantion**: the `PYTHONPATH` environment varible will make the birdears module be executed from that especified directory, having preemptiness even if there is already another version installed via `pip`.

## Running

After installing just run:

`birdears --help`

## Keybindings

The following keyboard diagrams should give you an idea on how the keybindings work. Please
note how the keys on the line from `z` (*unison*) to `,` (comma, *octave*) represent the notes
that are *natural* to the mode, and the line above represent the chromatics.

Also, for exercises with two octaves, the **uppercased keys represent the second octave**. For
example, `z` is *unison*, `,` is the *octave*, `Z` (uppercased) is the *double octave*. The same
for all the other intervals.

### Ionian (Major)

These are the keybindings for the **Ionian (Major) Scale**; black keys are the chromatic notes.

![birdears - ionian(major) keybindings](https://github.com/iacchus/birdears/raw/master/docs/keybindings/ionian.png)

### Dorian

![birdears - dorian keybindings](https://github.com/iacchus/birdears/raw/master/docs/keybindings/dorian.png)

### Phrygian

![birdears - phryigian keybindings](https://github.com/iacchus/birdears/raw/master/docs/keybindings/phrygian.png)

### Lydian

![birdears - lydian keybindings](https://github.com/iacchus/birdears/raw/master/docs/keybindings/lydian.png)

### Mixolydian

![birdears - mixolydian keybindings](https://github.com/iacchus/birdears/raw/master/docs/keybindings/mixolydian.png)

### Aeolian (minor)

![birdears - aeolian keybindings](https://github.com/iacchus/birdears/raw/master/docs/keybindings/minor.png)

### Locrian

![birdears - locrian(minor) keybindings](https://github.com/iacchus/birdears/raw/master/docs/keybindings/locrian.png)

## Advanced

![birdears - advanced keybindings](https://github.com/iacchus/birdears/raw/master/docs/keybindings/full-advanced.png)

*this is still being improved*

Legend for the keys on the diagram above:

| Text  Format       | Scale Direction | Octave                             |
|--------------------|-----------------|------------------------------------|
| blue (bold italic) | descending      | second octave (shift or caps lock) |
| pink (bold)        | descending      | first octave                       |
| black/white (bold) | ascending       | first octave                       |
| black (italic)     | ascending       | second octave (shift or caps lock) |

**White keys** are the diatonic notes, **black keys** are the chromatic ones.

Descendent mode are usable for exercises with `-d` or `--descendent`.

Chromatic keys are usable for exercises with `-c` or `--chromatic`.

Second octave is usable for exercises with `-n 2` or `--n_octaves 2`

## Documentation

Full documentation for this software is available at birdears [Read The Docs](https://birdears.readthedocs.io/en/latest/)
and also in [PDF format](https://github.com/iacchus/birdears/raw/master/docs/sphinx/_build/latex/birdears.pdf).

## Contributing

Those who want to contribute to this project can read [CONTRIBUTING.md](CONTRIBUTING.md).

## Etc

the screencast was recorded with a command similar to

```
COLUMNS=120 LINES=36 ttyrec
seq2gif -s 2 -i ttyrecord -w 120 -h 36 -o use.gif
```

[ttyrec](https://aur.archlinux.org/packages/ttyrec/) and [seq2gif](https://github.com/saitoha/seq2gif)

keyboard layouts were generated with http://www.keyboard-layout-editor.com/
