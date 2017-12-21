# birdears

## TODO

### Classes

Classes:

[maybe] Make a class for response (to be used by question.check\_question)

### Documentation

Method theory

Music theory

Presets

Interactive use with Jupyter

#### Installing

* `git clone` repo and run with `python -m birdears` from repo's root

### Features

Make somehing for improvising on pre-made harmonies

Plugins/extensions, easy way of users extending the software by using the api,
maybe providing frontend tools

Track correct/wrong answers by type, mode, tonic, date etc, maybe using sqlite3
db so that the user can track it's progress.

Pre-chosen number of questions (20 for example.) with percent of success.

### Prequestion Method

I triad.

### Resolution methods

Note-\>tonic (for dictation): 1st note then tonic, 2nd note then tonic, 3th note then tonic, 4th note then tonic.

Notes playing along with cadence (for dictation)

### Refactoring

Encapsulate birdears.interfaces.commandline in a class.

We should use some random() method inside Interval to select some random
interval or namethe class as RandomInterval. First option is best and we should
be able to generate not random interval using Interval class.

Maybe register question classes in a global.

Maybe sequence can contain sequences play(): if type==sequence, then play()

GUI: we should do one widget for each type of exercise.

We can make sequence not musical agnostics, ie., containing only strings for notes
and chords, but alo semitones so that play() can send this for threaded UI
callbacks.

### Etc

*none*
