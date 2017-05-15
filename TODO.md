# birdears

## todo

### classes

classes: ~~interval~~ :tada:, cadence and ~~resolution~~ ✓, maybe ~~scale~~
(done :tada:.)

make a class for response (by check_question)

### documentation

write documentation in docstrings using Google style docstrings

### features

different cadences

~~implement harmonic intervals~~ ✓

~~melodic dictation~~ ✓ :tada:, ~~computer and~~ instrumental (time based,
to be played on instrument)

~~bindings with argparse~ click ✓

plugins/extensions, easy way of users extending the software by using the api,
maybe providing frontend tools

configure it with a toml file, which will send parameters by the question class
with a dict/config file.

think on an interface, or a well written api that allows many interfaces:
cli (maybe centering things); tui (urwid); gui (kivy)

logging

improve live debugging options

we need to allow less than one octave / only certain interval,
eg.: I to IV, V to VIII etc

track correct/wrong answers by type, mode, tonic, date etc, aybe using sqlite3
db so that the user can track it's progress

# refactoring

~~change global names~~ ✓

we should think in a better algo for melodic dictation; currently always begins
with tonic; maybe playing a cadence with I-V-IV-I triads then choosing random
intervals w/ or w/out tonic.

we should use some kind of config object to configure exercises, as they have
an extensive number of parameters and there are more to come.

note: maybe you find this useful https://gist.github.com/rxaviers/7360908

refactore keys so that they dnn't give double sharps or double flats
