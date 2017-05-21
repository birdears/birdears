# birdears

## TODO

### Classes

Classes:

* ~~interval~~ :tada:,
* ~~cadence~~(Sequence can generate Progressions ✓) and
* ~~resolution~~ ✓, maybe
* ~~scale~~ (done :tada:.)

**[maybe] Make a class for response (to be used by question.check\_question)**

### Documentation

~~Write documentation in docstrings using Google style docstrings.~~

~~Improve `click` CLI help documentation.~~

### Features

~~Different cadences.~~ :tada: Sequence: chord progressions; PreQuestion class

~~implement harmonic intervals~~ ✓

* ~~melodic dictation~~ ✓ :tada:,
  * ~~computer~~ and
  * ~~instrumental (time based, to be played on instrument)~~ ✓

~~bindings with argparse~~ click ✓

**plugins/extensions, easy way of users extending the software by using the api,
maybe providing frontend tools**

~~configure it with a toml file, which will send parameters by the question
class with a dict/config file.~~ ✓ :tada:

think on an interface, or a well written api that allows many interfaces:

* ~~cli (maybe centering things)~~ ✓;
* **tui (urwid);**
* **gui (kivy)**

**logging**

**improve live debugging options**

*~~we need to allow less than one octave / only certain interval,
eg.: I to IV, V to VIII etc~~* :tada: :gift: valid_intervals

**track correct/wrong answers by type, mode, tonic, date etc, maybe using sqlite3
db so that the user can track it's progress.**

Question base should accept aarguments intelligently, for example, ~~`tonic` can
be a string or a list~~, or a tuple, so he can sort one of the elements as tonic;
~~`octave` can be int or tuple, so that the octave will be chosen randomly by that
range~~, etc. This will give us tools to load questions from config files.

**question, resolution, pre-qestion: duration, delay and post delay should be
configurable via options too.**

### Refactoring

~~change global names~~ ✓

~~we should think in a better algo for melodic dictation; currently always begins
with tonic; maybe playing a cadence with I-V-IV-I triads then choosing random
intervals w/ or w/out tonic.~~ PreQuestion class ✓ :tada:

**We should use some kind of config object to configure exercises, as they have
an extensive number of parameters and there are more to come.**

note: maybe you'd find this useful https://gist.github.com/rxaviers/7360908

~~Refactor keys so that they didn't give double sharps or double flats.~~ ✓
:tada: CIRCLE\_OF\_FIFTHS !

**Maybe refactor make\_resoltion/sequence as generator so that we can interact
with the UI, (eg., every note played in resolution is highlighted in user
interface.)**

**Encapsulate birdears.interfaces.commandline in a class.**

**We should use some random() method inside Interval to select some random
interval or namethe class as RandomInterval. First option is best and we should
be able to generate not random interval using Interval class.**

**Maybe register question classes in a global.**

~~Meybe we could avoid using collections.deque to support older python 3
versions in birdears.scale.~~ ✓

**Maybe sequence elements should be a tuple so to have each element the ability
of handling its own duration, ldelay time, this way:
`('C4', 2, 3)` or `(['C4','E4',"G4"], 1, 2)` ... `(element, duration, delay)`**

**Maybe sequence can contain sequences play(): if type=sequence, then play()**

### Etc

**Lets reserve options to `-r` to `--resolution` method  (FET-like, Repeat-only,
Inverted-question) ans `-p` to`--pre-question` (I-IV-V-I, Tonic-Interval, etc,
ie., tonic affirmation before question.)**
