# birdears

[![Maintenance](https://img.shields.io/maintenance/yes/2017.svg?style=flat-square)](https://github.com/iacchus/birdears/issues/new?title=Is+birdears+still+maintained&body=Please+file+an+issue+if+the+maintained+button+says+no)
[![Travis Build Status](https://img.shields.io/travis/iacchus/birdears.svg?style=flat-square&label=build)](https://travis-ci.org/iacchus/birdears)
[![Coveralls](https://img.shields.io/coveralls/iacchus/birdears.svg?style=flat-square&label=coverage)](https://coveralls.io/github/iacchus/birdears)
[![Awesome Sheet Music](https://img.shields.io/badge/awesome-sheet%20music-blue.svg?style=flat-square&logoWidth=14;&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA%2FwD%2FAP%2BgvaeTAAAACXBIWXMAAD2EAAA9hAHVrK90AAAAB3RJTUUH4QYVEQ4dGSq4mgAAAuVJREFUKM8FwUtoHGUAB%2FD%2F983s7CSb7s6%2BsrtJtqbEJA21llgQi4VaCL5QRKXQg6JXEUTqrfQi9CTozYPeUgrtxceh1kbEEEtBeslzTbdrup109r2zMzvZ2Xl8s9%2F4%2B5Hvfg4vOGpzqJf3aCpY%2FfTMi5OvE%2B6mdx%2Fud0YjP5PNxpiuh6X9%2F3I%2F6mzcScvT%2BvjYCUucknhkYSnvNYTvr5169YNLCEMAHKfPvZxwrBZaqoaGWn%2BNBNWlJ4dzn3147n2totckelwZhdr%2B9U%2FOvnnx0kRSgTJdhOBpIPYzSMyE7DaQJEcoFOO5lFK%2BeszcjxblGU%2BUzHosO5%2B6Ek2kQUYuupt3cXxxEoTIYN0WFDGHNnGwvVFGLJ1eXqv%2B8dzJPK%2FRhvbLKwtnzoI7BvyBjqBzCGEiC5ougAgCCJUAymHZPuYWc8J27cGV3c76jOgM9FlwjpE7APMZAscHH%2FYQsBgAhqBvYCyeREgRbm%2FV3aXixLwf6DFxqpCIDpqPQMQIjNoTBLaN9uYO7v30T9h72sHlL1fIV1%2Bvh0mBsp16na6czmUuJM5XaM%2Fo5UEp9JqGeGEO7tBHfGYW73x8kay8%2FTwRvADL02PIClw6shkxbd8sxl%2Fo0yghVl%2FvIyoL0DY30G8ZcKt7kDnDVDGHQbOFNAFZzlC4ozDiub6SofGAWsNIZWh10X7WwtODNsyeh15ZhfVYw6M%2Ft9Do%2B1jdMsPAC%2BEEHCyAy5WCT5VE%2FqDyr4rh0IZlu%2BygZg%2FdaAw2O0KTUWh%2FVXBe4kT1KVgIeAPh1rHxJBdufHsnKJXvXK7slIV61SodNI7iswVRDgnB%2FEuz8IiDvs1xs2yH1Q099oaZfyj5lkRVf4Ta4%2B69vuF6ajeodkRJ2tzroVRq4%2F5v2xiTFahd115ITn5eu23L5on3mBn5O0UNTxB2m%2FIDdZD5hiUW7qcyhd%2B%2F%2BHUNc2%2B9i8OBwFfXDo11Hfjho2t3I4tRIRoYNBAV738fRoHSSCa2GwAAAABJRU5ErkJggg%3D%3D)](https://iacchus.github.io/awesome-sheet-music/)

[![GitHub (pre-)release](https://img.shields.io/github/release/iacchus/birdears/all.svg?style=flat-square)](https://github.com/iacchus/birdears/releases)
[![PyPI Status](https://img.shields.io/pypi/status/birdears.svg?style=flat-square&label=pypi-status)](https://pypi.python.org/pypi/birdears)
[![PyPI Version](https://img.shields.io/pypi/v/birdears.svg?style=flat-square)](https://pypi.python.org/pypi/birdears)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/birdears.svg?style=flat-square)](https://pypi.python.org/pypi/birdears)
[![Documentation Status](https://img.shields.io/badge/readthedocs-latest-orange.svg?style=flat-square)](https://birdears.readthedocs.io/en/latest/)

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
- [Running](#running)
- [Modes](#modes)
	- [melodic](#melodic)
	- [harmonic](#harmonic)
	- [dictation](#dictation)
	- [instrumental](#instrumental)
- [Loading from preset files](#loading-from-preset-files)
- [Contributing](#contributing)

<!-- /TOC -->

For the support chat, please `/join` [`#birdears`](http://webchat.freenode.net/?randomnick=1&channels=%23birdears&uio=MTY9dHJ1ZSYxMT0yNDY57) channel on freenode (`chat.freenode.net/6697` - ssl).

![birdears screencast](use.gif)

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

### Features

* questions
* pretty much configurable
* load from config file
* you can make your own presets
* can be used interactively *(docs needed)*
* can be used as a library *(docs needed)*

## Installing

### Installing the dependencies

`birdears` depends only on `python >= 3.5` and `sox` (which should be installed by your distribution's package manager,
supposing you're using linux, and which provides the `play` command.) 

#### Arch Linux

```
sudo pacman -Syu sox python python-pip
```

### Installing birdears

`pip install --user --upgrade --no-cache-dir birdears`

#### In-depth installation

You can choose to use a virtualenv to use birdears; this should give you an idea on how to setup one virtualenv.

You should first install virtualenv (for python3) using your distribution's package (supposing you're on linux),
then on terminal:

```
virtualenv -p python3 ~/.venv # use the directory ~/.venv/ for the virtualenv

~/.venv/bin/activate          # activate the virtualenv; this should be done
                              # every time you may want to run the software
                              # installed here.

pip3 install birdears         # this will install the software

birdears --help               # and this will run it
```

## Running

After installing just run:

`birdears --help`

## Modes

### melodic

#### Description

In this exercise birdears will play two notes, the tonic and the interval
melodically, ie., one after the other and you should reply which is the
correct distance between the two.

#### Command-line options

```
Usage: birdears melodic [options]

  Melodic interval recognition

Options:
  -m, --mode <mode>               Mode of the question.
  -t, --tonic <tonic>             Tonic of the question.
  -o, --octave <octave>           Octave of the question.
  -d, --descending                Whether the question interval is descending.
  -c, --chromatic                 If chosen, question has chromatic notes.
  -n, --n_octaves <n max>         Maximum number of octaves.
  -v, --valid_intervals <1,2,..>  A comma-separated list without spaces
                                  of valid scale degrees to be chosen for the
                                  question.
  -q, --user_durations <1,0.5,n..>
                                  A comma-separated list without
                                  spaces with PRECISLY 9 floating values. Or
                                  'n' for default              duration.
  -p, --prequestion_method <prequestion_method>
                                  The name of a pre-question method.
  -r, --resolution_method <resolution_method>
                                  The name of a resolution method.
  -h, --help                      Show this message and exit.

  In this exercise birdears will play two notes, the tonic and the interval
  melodically, ie., one after the other and you should reply which is the
  correct distance between the two.

  Valid values are as follows:

  -m <mode> is one of: major, dorian, phrygian, lydian, mixolydian, minor,
  locrian

  -t <tonic> is one of: A, A#, Ab, B, Bb, C, C#, D, D#, Db, E, Eb, F, F#, G,
  G#, Gb

  -p <prequestion_method> is one of: none, tonic_only, progression_i_iv_v_i

  -r <resolution_method> is one of: nearest_tonic, repeat_only
```

### harmonic

#### Description

In this exercise birdears will play two notes, the tonic and the interval
harmonically, ie., both on the same time and you should reply which is the
correct distance between the two.


#### Command-line options

```
Usage: birdears harmonic [options]

  Harmonic interval recognition

Options:
  -m, --mode <mode>               Mode of the question.
  -t, --tonic <note>              Tonic of the question.
  -o, --octave <octave>           Octave of the question.
  -d, --descending                Whether the question interval is descending.
  -c, --chromatic                 If chosen, question has chromatic notes.
  -n, --n_octaves <n max>         Maximum number of octaves.
  -v, --valid_intervals <1,2,..>  A comma-separated list without spaces
                                  of valid scale degrees to be chosen for the
                                  question.
  -q, --user_durations <1,0.5,n..>
                                  A comma-separated list without
                                  spaces with PRECISLY 9 floating values. Or
                                  'n' for default              duration.
  -p, --prequestion_method <prequestion_method>
                                  The name of a pre-question method.
  -r, --resolution_method <resolution_method>
                                  The name of a resolution method.
  -h, --help                      Show this message and exit.

  In this exercise birdears will play two notes, the tonic and the interval
  harmonically, ie., both on the same time and you should reply which is the
  correct distance between the two.

  Valid values are as follows:

  -m <mode> is one of: major, dorian, phrygian, lydian, mixolydian, minor,
  locrian

  -t <tonic> is one of: A, A#, Ab, B, Bb, C, C#, D, D#, Db, E, Eb, F, F#, G,
  G#, Gb

  -p <prequestion_method> is one of: none, tonic_only, progression_i_iv_v_i

  -r <resolution_method> is one of: nearest_tonic, repeat_only
```

### dictation

#### Description

In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should reply the correct intervals of the
melodic dictation.

#### Command-line options

```
Usage: birdears dictation [options]

  Melodic dictation

Options:
  -m, --mode <mode>               Mode of the question.
  -i, --max_intervals <n max>     Max random intervals for the dictation.
  -x, --n_notes <n notes>         Number of notes for the dictation.
  -t, --tonic <note>              Tonic of the question.
  -o, --octave <octave>           Octave of the question.
  -d, --descending                Wether the question interval is descending.
  -c, --chromatic                 If chosen, question has chromatic notes.
  -n, --n_octaves <n max>         Maximum number of octaves.
  -v, --valid_intervals <1,2,..>  A comma-separated list without spaces
                                  of valid scale degrees to be chosen for the
                                  question.
  -q, --user_durations <1,0.5,n..>
                                  A comma-separated list without
                                  spaces with PRECISLY 9 floating values. Or
                                  'n' for default              duration.
  -p, --prequestion_method <prequestion_method>
                                  The name of a pre-question method.
  -r, --resolution_method <resolution_method>
                                  The name of a resolution method.
  -h, --help                      Show this message and exit.

  In this exercise birdears will choose some random intervals and create a
  melodic dictation with them. You should reply the correct intervals of the
  melodic dictation.

  Valid values are as follows:

  -m <mode> is one of: major, dorian, phrygian, lydian, mixolydian, minor,
  locrian

  -t <tonic> is one of: A, A#, Ab, B, Bb, C, C#, D, D#, Db, E, Eb, F, F#, G,
  G#, Gb

  -p <prequestion_method> is one of: none, tonic_only, progression_i_iv_v_i

  -r <resolution_method> is one of: nearest_tonic, repeat_only
```

### instrumental

#### Description

In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should play the correct melody in you
musical instrument.

#### Command-line options

```
Usage: birdears instrumental [options]

  Instrumental melodic time-based dictation

Options:
  -m, --mode <mode>               Mode of the question.
  -w, --wait_time <seconds>       Time in seconds for next question/repeat.
  -u, --n_repeats <times>         Times to repeat question.
  -i, --max_intervals <n max>     Max random intervals for the dictation.
  -x, --n_notes <n notes>         Number of notes for the dictation.
  -t, --tonic <note>              Tonic of the question.
  -o, --octave <octave>           Octave of the question.
  -d, --descending                Wether the question interval is descending.
  -c, --chromatic                 If chosen, question has chromatic notes.
  -n, --n_octaves <n max>         Maximum number of octaves.
  -v, --valid_intervals <1,2,..>  A comma-separated list without spaces
                                  of valid scale degrees to be chosen for the
                                  question.
  -q, --user_durations <1,0.5,n..>
                                  A comma-separated list without
                                  spaces with PRECISLY 9 floating values. Or
                                  'n' for default              duration.
  -p, --prequestion_method <prequestion_method>
                                  The name of a pre-question method.
  -r, --resolution_method <resolution_method>
                                  The name of a resolution method.
  -h, --help                      Show this message and exit.

  In this exercise birdears will choose some random intervals and create a
  melodic dictation with them. You should play the correct melody in you
  musical instrument.

  Valid values are as follows:

  -m <mode> is one of: major, dorian, phrygian, lydian, mixolydian, minor,
  locrian

  -t <tonic> is one of: A, A#, Ab, B, Bb, C, C#, D, D#, Db, E, Eb, F, F#, G,
  G#, Gb

  -p <prequestion_method> is one of: none, tonic_only, progression_i_iv_v_i

  -r <resolution_method> is one of: nearest_tonic, repeat_only
```

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

## Etc

the screencast was recorded with a command similar to

```
COLUMNS=120 LINES=36 ttyrec
seq2gif -s 2 -i ttyrecord -w 120 -h 36 -o use.gif
```

[ttyrec](https://aur.archlinux.org/packages/ttyrec/) and [seq2gif](https://github.com/saitoha/seq2gif)
