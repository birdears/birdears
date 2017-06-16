# birdears documentation

## Contents

* [birdears API](birdears.rst)

```eval_rst

.. toctree::
   :maxdepth: 3

   index.md
   birdears.rst
```

## What is Functional Ear Training

### The method

Testing abc

```abc
X: 1
T: Banish Misfortune
R: jig
M: 6/8
L: 1/8
K: Dmix
fed cAG| A2d cAG| F2D DED| FEF GFG|
AGA cAG| AGA cde|fed cAG| Ad^c d3:|
f2d d^cd| f2g agf| e2c cBc|e2f gfe|
f2g agf| e2f gfe|fed cAG|Ad^c d3:|
f2g e2f| d2e c2d|ABA GAG| F2F GED|
c3 cAG| AGA cde| fed cAG| Ad^c d3:|
```

## birdears modes

birdears actually has four modes:

* melodic interval question
* harmonic interval question
* melodic dictation question
* instrumental dictation question

### basic usage

To see the commands avaliable just invoke the command without any arguments:

```
birdears
```

```
$ birdears
Usage: birdears  <command> [options]

  birdears ─ Functional Ear Training for Musicians!

Options:
  -h, --help  Show this message and exit.

Commands:
  dictation     Melodic dictation
  harmonic      Harmonic interval recognition
  instrumental  Instrumental melodic time-based dictation
  melodic       Melodic interval recognition

  You can use '<command> --help' to show options for a specific command.
```

There are four commands, which are `dictation`, `harmonic`, `instrumental` and
`melodic`.

You can play the default question for these by starting birdears with one of
these commands, or you can check the `--help` for additional options for each
of the commands, invoking this way:

```
birdears <command> --help
```

### melodic

In this exercise birdears will play two notes, the tonic and the interval
melodically, ie., one after the other and you should reply which is the
correct distance between the two.

```
birdears melodic --help
```

```
$ birdears melodic --help
Usage: birdears melodic [options]

  Melodic interval recognition

Options:
  -m, --mode [major|minor]  Mode of the question.
  -t, --tonic <note>        Tonic of the question.
  -o, --octave <octave>     Octave of the question.
  -d, --descending          Whether the question interval is descending.
  -c, --chromatic           If chosen, question has chromatic notes.
  -n, --n_octaves <n max>   Maximum number of octaves.
  -h, --help                Show this message and exit.

  In this exercise birdears will play two notes, the tonic and the interval
  melodically, ie., one after the other and you should reply which is the
  correct distance between the two.
```

### harmonic

In this exercise birdears will play two notes, the tonic and the interval
harmonically, ie., both on the same time and you should reply which is the
correct distance between the two.

```
birdears harmonic --help
```

```
$ birdears harmonic --help
Usage: birdears harmonic [options]

  Harmonic interval recognition

Options:
  -m, --mode [major|minor]  Mode of the question.
  -t, --tonic <note>        Tonic of the question.
  -o, --octave <octave>     Octave of the question.
  -d, --descending          Whether the question interval is descending.
  -c, --chromatic           If chosen, question has chromatic notes.
  -n, --n_octaves <n max>   Maximum number of octaves.
  -h, --help                Show this message and exit.

  In this exercise birdears will play two notes, the tonic and the interval
  harmonically, ie., both on the same time and you should reply which is the
  correct distance between the two.
```

### dictation

In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should reply the correct intervals of the
melodic dictation.

```
birdears dictation --help
```

```
$ birdears dictation --help
Usage: birdears dictation [options]

  Melodic dictation

Options:
  -m, --mode [major|minor]     Mode of the question.
  -i, --max_intervals <n max>  Max random intervals for the dictation.
  -x, --n_notes <n notes>      Number of notes for the dictation.
  -t, --tonic <note>           Tonic of the question.
  -o, --octave <octave>        Octave of the question.
  -d, --descending             Wether the question interval is descending.
  -c, --chromatic              If chosen, question has chromatic notes.
  -n, --n_octaves <n max>      Maximum number of octaves.
  -h, --help                   Show this message and exit.

  In this exercise birdears will choose some random intervals and create a
  melodic dictation with them. You should reply the correct intervals of the
  melodic dictation.
```

### instrumental

In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should play the correct melody in you
musical instrument.

```
birdears instrumental --help
```

```
$ birdears instrumental --help
Usage: birdears instrumental [options]

  Instrumental melodic time-based dictation

Options:
  -m, --mode [major|minor]     Mode of the question.
  -w, --wait_time <seconds>    Time in seconds for next question/repeat.
  -u, --n_repeats <times>      Times to repeat question.
  -i, --max_intervals <n max>  Max random intervals for the dictation.
  -x, --n_notes <n notes>      Number of notes for the dictation.
  -t, --tonic <note>           Tonic of the question.
  -o, --octave <octave>        Octave of the question.
  -d, --descending             Wether the question interval is descending.
  -c, --chromatic              If chosen, question has chromatic notes.
  -n, --n_octaves <n max>      Maximum number of octaves.
  -h, --help                   Show this message and exit.

  In this exercise birdears will choose some random intervals and create a
  melodic dictation with them. You should play the correct melody in you
  musical instrument.
```
