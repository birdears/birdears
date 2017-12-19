######################
birdears documentation
######################

Welcome to birdears documentation.

``birdears`` is a software written in Python 3 for ear training for
musicians (musical intelligence, transcribing music, composing). It is a
clone of the method used by `Funcitional Ear
Trainer <https://play.google.com/store/apps/details?id=com.kaizen9.fet.android>`__
app for Android.

It comes with four modes, or four kind of exercises, which are:
``melodic``, ``harmonic``, ``dictation`` and ``instrumental``.

In resume, with the *melodic* mode two notes are played one after the
other and you have to guess the interval; with the *harmonic* mode,
two notes are played simoutaneously (harmonically) and you should guess
the interval.

With the *dictation* mode, more than 2 notes are played (*ie*., a
melodic dictation) and you should tell what are the intervals between
them.

With the *instrumental* mode, it is a like the *dictation*, but you will
be expected to play the notes on your instrument, *ie*., birdears will
not wait for a typed reply and you should prectice with your own
judgement. The melody can be repeat any times and you can have as much
time as you want to try it out.

.. toctree::
   :maxdepth: 3

   installing
   using
   birdears
   birdears.questions

.. include:: installing.rst

.. include:: using.rst

API
^^^

.. include:: birdears.rst

.. include:: birdears.questions.rst

.. include:: birdears.interfaces.rst
