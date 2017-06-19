BirdEars
========

|Maintenance| |Travis Build Status| |Coveralls| |Codecov| |Code Climate
coverage| |Code Climate issues| |Code Climate gpa| |Gitter|

|GitHub (pre-)release| |PyPI Status| |PyPI Version| |PyPI Python
Versions| |Waffle.io| |GitHub issues| |Documentation Status|

.. raw:: html

   <!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

-  `Introduction <#introduction>`__

   -  `birdears <#birdears>`__
   -  `What is musical ear training <#what-is-musical-ear-training>`__
   -  `Features <#features>`__

-  `Installing <#installing>`__

   -  `Installing the dependencies <#installing-the-dependencies>`__

      -  `Arch Linux <#arch-linux>`__

   -  `Installing birdears <#installing-birdears>`__

      -  `In-depth installation <#in-depth-installation>`__

-  `Running <#running>`__
-  `Modes <#modes>`__

   -  `melodic <#melodic>`__

      -  `Description <#description>`__
      -  `Command-line options <#command-line-options>`__

   -  `harmonic <#harmonic>`__

      -  `Description <#description>`__
      -  `Command-line options <#command-line-options>`__

   -  `dictation <#dictation>`__

      -  `Description <#description>`__
      -  `Command-line options <#command-line-options>`__

   -  `instrumental <#instrumental>`__

      -  `Description <#description>`__
      -  `Command-line options <#command-line-options>`__

-  `Loading from preset files <#loading-from-preset-files>`__

   -  `Pre-made presets <#pre-made-presets>`__

      -  `Pre-made presets
         description <#pre-made-presets-description>`__

   -  `Creating new preset files <#creating-new-preset-files>`__

-  `Contributing <#contributing>`__

.. raw:: html

   <!-- /TOC -->

Introduction
------------

birdears
~~~~~~~~

``birdears`` is a software written in Python 3 for ...

What is musical ear training
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is a method..

Features
~~~~~~~~

-  questions
-  load from config file

Installing
----------

Installing the dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Arch Linux
^^^^^^^^^^

::

    sudo pacman -Syu sox python python-pip

Installing birdears
~~~~~~~~~~~~~~~~~~~

``pip install --user --upgrade birdears``

In-depth installation
^^^^^^^^^^^^^^^^^^^^^

Running
-------

After installing just run:

``birdears --help``

Modes
-----

melodic
~~~~~~~

Description
^^^^^^^^^^^

In this exercise birdears will play two notes, the tonic and the
interval melodically, ie., one after the other and you should reply
which is the correct distance between the two.

Command-line options
^^^^^^^^^^^^^^^^^^^^

::

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

      -t <tonic> is one of: A, A#, Ab, B, Bb, C, C#, Cb, D, D#, Db, E, Eb, F,
      F#, Fb, G, G#, Gb

      -p <prequestion_method> is one of: none, tonic_only, progression_i_iv_v_i

      -r <resolution_method> is one of: nearest_tonic, repeat_only

harmonic
~~~~~~~~

Description
^^^^^^^^^^^

Command-line options
^^^^^^^^^^^^^^^^^^^^

::

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

      -t <tonic> is one of: A, A#, Ab, B, Bb, C, C#, Cb, D, D#, Db, E, Eb, F,
      F#, Fb, G, G#, Gb

      -p <prequestion_method> is one of: none, tonic_only, progression_i_iv_v_i

      -r <resolution_method> is one of: nearest_tonic, repeat_only

dictation
~~~~~~~~~

Description
^^^^^^^^^^^

In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should reply the correct intervals of
the melodic dictation.

Command-line options
^^^^^^^^^^^^^^^^^^^^

::

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

      -t <tonic> is one of: A, A#, Ab, B, Bb, C, C#, Cb, D, D#, Db, E, Eb, F,
      F#, Fb, G, G#, Gb

      -p <prequestion_method> is one of: none, tonic_only, progression_i_iv_v_i

      -r <resolution_method> is one of: nearest_tonic, repeat_only

instrumental
~~~~~~~~~~~~

Description
^^^^^^^^^^^

In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should play the correct melody in you
musical instrument.

Command-line options
^^^^^^^^^^^^^^^^^^^^

::

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

      -t <tonic> is one of: A, A#, Ab, B, Bb, C, C#, Cb, D, D#, Db, E, Eb, F,
      F#, Fb, G, G#, Gb

      -p <prequestion_method> is one of: none, tonic_only, progression_i_iv_v_i

      -r <resolution_method> is one of: nearest_tonic, repeat_only

Loading from preset files
-------------------------

Pre-made presets
~~~~~~~~~~~~~~~~

Birdears cointains some pre-made presets in it's ``presets/``
subdirectory.

The study for beginners is recommended by following the numeric order of
those files (000, 001, then 002 etc.)

Pre-made presets description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Maybe these things would go better in the readhedocs documentation.

Creating new preset files
~~~~~~~~~~~~~~~~~~~~~~~~~

You can open the files cointained in birdears premade ``presets/``
folder to have an ideia on how config files are made; it is simply the
command line options written in a form ``toml`` standard.

Contributing
------------

Those who want to contribute to this project can read
`CONTRIBUTING.md <CONTRIBUTING.md>`__.

--------------

::

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

.. |Maintenance| image:: https://img.shields.io/maintenance/yes/2017.svg?style=flat
   :target: https://github.com/iacchus/birdears/issues/new?title=Is+birdears+still+maintained&body=Please+file+an+issue+if+the+maintained+button+says+no
.. |Travis Build Status| image:: https://img.shields.io/travis/iacchus/birdears.svg?style=flat&label=build
   :target: https://travis-ci.org/iacchus/birdears
.. |Coveralls| image:: https://img.shields.io/coveralls/iacchus/birdears.svg?style=flat&label=Coveralls
   :target: https://coveralls.io/github/iacchus/birdears
.. |Codecov| image:: https://img.shields.io/codecov/c/github/iacchus/birdears.svg?style=flat&label=Codecov
   :target: https://codecov.io/gh/iacchus/birdears
.. |Code Climate coverage| image:: https://img.shields.io/codeclimate/coverage/github/iacchus/birdears.svg?style=flat&label=Codeclimate
   :target: https://codeclimate.com/github/iacchus/birdears
.. |Code Climate issues| image:: https://img.shields.io/codeclimate/issues/github/iacchus/birdears.svg?style=flat&label=cclimate-issues
   :target: https://codeclimate.com/github/iacchus/birdears/issues
.. |Code Climate gpa| image:: https://img.shields.io/codeclimate/github/iacchus/birdears.svg?style=flat&label=cclimate-GPA
   :target: https://codeclimate.com/github/iacchus/birdears
.. |Gitter| image:: https://img.shields.io/gitter/room/birdears/Lobby.svg?style=flat
   :target: https://gitter.im/birdears/Lobby
.. |GitHub (pre-)release| image:: https://img.shields.io/github/release/iacchus/birdears/all.svg?style=flat
   :target: https://github.com/iacchus/birdears/releases
.. |PyPI Status| image:: https://img.shields.io/pypi/status/birdears.svg?style=flat&label=pypi-status
   :target: https://pypi.python.org/pypi/birdears
.. |PyPI Version| image:: https://img.shields.io/pypi/v/birdears.svg?style=flat
   :target: https://pypi.python.org/pypi/birdears
.. |PyPI Python Versions| image:: https://img.shields.io/pypi/pyversions/birdears.svg?style=flat
   :target: https://pypi.python.org/pypi/birdears
.. |Waffle.io| image:: https://img.shields.io/waffle/label/iacchus/birdears/in%20progress.svg?style=flat
   :target: https://waffle.io/iacchus/birdears
.. |GitHub issues| image:: https://img.shields.io/github/issues/iacchus/birdears.svg?style=flat&label=gh-issues
   :target: https://github.com/iacchus/birdears/issues
.. |Documentation Status| image:: https://readthedocs.org/projects/birdears/badge/?version=latest
   :target: https://birdears.readthedocs.io/en/latest/?badge=latest
