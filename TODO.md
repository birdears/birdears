# birdears

## todo

### classes

classes: ~~interval~~ :tada:, cadence and resolution(cadence), maybe ~~scale~~
(done :tada:.)

### documentation

write documentation in docstrings using [numydoc](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt#documenting-classes)

### features

different cadences

~~implement harmonic intervals~~ ✓

~~melodic dictation~~ ✓ :tada:, ~~computer and~~ instrumental (time based,
to be played on instrument)

bindings with argparse

plugins/extensions, easy way of users extending the software by using the api,
maybe providing frontend tools

configure it with a toml file, which will send parameters by the question class
with a dict/config file.

# refactoring

~~change global names~~ ✓
we should think in a better algo for melodic dictation; currently always begins
with tonic; maybe playing a cadence with I-V-IV-I triads then choosing random
intervals w/ or w/out tonic.

we should use some kind of config object to configure exercises, as they have an
extensive number of parameters and there are more to come.
