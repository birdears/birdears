BirdEars
========

|Travis Build Status| |Coveralls| |Codecov| |Code Climate coverage|
|Code Climate issues| |Code Climate gpa| |Gitter|

|PyPI Status| |PyPI Version| |PyPI Python Versions| |Waffle.io|
|Documentation Status|

Functional Ear Training for Musicians
-------------------------------------

In current development though functional. Uses python 3 and
`sox <http://sox.sourceforge.net/>`__.

Usage
-----

1. Install the Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install ``sox`` and ``python3`` (see
`below <https://github.com/iacchus/birdears#installing--dependencies>`__)
and,

2. clone the repository
~~~~~~~~~~~~~~~~~~~~~~~

::

    git clone https://github.com/iacchus/birdears.git

3. and just run the package's **main**:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    python3 -m birdears

Keybindings for intervals
-------------------------

**MAJOR keyboard keys** (with *chromatics*)

Key Index for major and chromatic major context

::

      keyboard              would represent

     s d   g h j        IIb  IIIb       Vb VIb  VIIb
    z x c v b n m  <-  I   II   III  IV   V   VI   VII

*(**SHIFT** key meaning an octave higher)*

**MINOR keyboard keys** (with *chromatics*)

Key index for minor and chromatic minor context

::

       keyboard                 would represent
                               in chromatics in
                                'a' minor context

     s   f g   j k   eg.:      a#   c# d#    f# g#
    z x c v b n m    -------  a  b c  d  e  f  g

Screenshot or didn't happen
---------------------------

*(development version)*

.. figure:: https://i.imgur.com/PSZCL2a.png
   :alt: birsears screenshot

   birsears screenshot

Other keys
~~~~~~~~~~

+-------+---------------------------------+
| Key   | What it Does                    |
+=======+=================================+
| q     | quit.                           |
+-------+---------------------------------+
| r     | to repeat the tonic/interval.   |
+-------+---------------------------------+

Installing Dependencies
-----------------------

Submit your distro's too..

Arch Linux
~~~~~~~~~~

::

    sudo pacman -S python sox

Contributing
------------

Coding
~~~~~~

We ask for people who wants to contribute for the code to look to the
musical side first,

Checking code style
^^^^^^^^^^^^^^^^^^^

We use `pep8 <https://pypi.python.org/pypi/pep8>`__ to check code
formatting:

::

    pep8 birdears --exclude=click

Module Documentation
~~~~~~~~~~~~~~~~~~~~

Our documentation is online at
`readthedocs <http://birdears.readthedocs.io>`__.

We are using Sphinx to generate documentation for this module. The
sphinx resource files are in the ``docs/sphinx/`` directory.

We use Google Style Docstrings to write documentation for the API. Here
is Google's online `Python Style
Guide <https://google.github.io/styleguide/pyguide.html>`__ which has
some of the specification or Sphinx Napoleon documentation
`online <http://www.sphinx-doc.org/en/stable/ext/napoleon.html>`__ or in
`PDF <https://readthedocs.org/projects/sphinxcontrib-napoleon/downloads/pdf/latest/>`__.
Napoleon is the extension used by Sphinx to render Google Docstrings in
the documentation.

Runing apidoc
^^^^^^^^^^^^^

We want to exclude third-party module ``click`` when generating
automatic documentation for the package:

::

    sphinx-apidoc -o docs/sphinx/_apidoc birdears/ birdears/click/

End-user Documentation
~~~~~~~~~~~~~~~~~~~~~~

We aim to build a method / music theory together with this software,
maybe in the GitHub repo's wiki.

Writing Tests
~~~~~~~~~~~~~

We use `pytest <https://docs.pytest.org/en/latest/>`__ to run tests; we
use `coverage.py <https://coverage.readthedocs.io>`__ to report code
coverage;

::

    coverage run --source=birdears --module pytest --verbose tests/

We use `coveralls <https://coveralls.io/github/iacchus/birdears>`__ and
`Travis CI <https://travis-ci.org/iacchus/birdears>`__.

Out tests are in repo's ``tests/`` directory.

Feature requests :gift: and suggestions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You are welcome to use `github
issues <https://github.com/iacchus/birdears/issues>`__ or
`gitter.im <https://gitter.im/birdears/Lobby>`__ to ask for, or give
ideia for new features.

Other stuff
-----------

We are using pandoc to convert README from .md to .rst:

::

    pandoc --from=markdown --to=rst README.md -o README.rst

To generate package for PyPI:

::

    python setup.py sdist
    python setup.py bdist_wheel

To publish to PyPI:

::

    twine upload dist/*

`PEP 8 <https://pep8.org>`__ — the Style Guide for Python Code

`Python.org PEP8 <https://www.python.org/dev/peps/pep-0008/>`__

.. |Travis Build Status| image:: https://img.shields.io/travis/iacchus/birdears.svg?label=build
   :target: https://travis-ci.org/iacchus/birdears
.. |Coveralls| image:: https://img.shields.io/coveralls/iacchus/birdears.svg?label=Coveralls
   :target: https://coveralls.io/github/iacchus/birdears
.. |Codecov| image:: https://img.shields.io/codecov/c/github/iacchus/birdears.svg?label=Codecov
   :target: https://codecov.io/gh/iacchus/birdears
.. |Code Climate coverage| image:: https://img.shields.io/codeclimate/coverage/github/iacchus/birdears.svg?label=Codeclimate
   :target: https://codeclimate.com/github/iacchus/birdears
.. |Code Climate issues| image:: https://img.shields.io/codeclimate/issues/github/iacchus/birdears.svg?label=issues
   :target: https://codeclimate.com/github/iacchus/birdears/issues
.. |Code Climate gpa| image:: https://img.shields.io/codeclimate/github/iacchus/birdears.svg?label=GPA
   :target: https://codeclimate.com/github/iacchus/birdears
.. |Gitter| image:: https://img.shields.io/gitter/room/birdears/Lobby.svg
   :target: https://gitter.im/birdears/Lobby
.. |PyPI Status| image:: https://img.shields.io/pypi/status/birdears.svg?label=PyPI+Status
   :target: https://pypi.python.org/pypi/birdears
.. |PyPI Version| image:: https://img.shields.io/pypi/v/birdears.svg
   :target: https://pypi.python.org/pypi/birdears
.. |PyPI Python Versions| image:: https://img.shields.io/pypi/pyversions/birdears.svg
   :target: https://pypi.python.org/pypi/birdears
.. |Waffle.io| image:: https://img.shields.io/waffle/label/iacchus/birdears/in%20progress.svg
   :target: https://waffle.io/iacchus/birdears
.. |Documentation Status| image:: https://readthedocs.org/projects/birdears/badge/?version=latest
   :target: http://birdears.readthedocs.io/en/latest/?badge=latest
