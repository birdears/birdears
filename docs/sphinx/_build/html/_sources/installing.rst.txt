Installing birdears
===================

Installing the dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Arch Linux
^^^^^^^^^^

::

    sudo pacman -Syu sox python python-pip

Installing birdears
~~~~~~~~~~~~~~~~~~~

``pip install --user --upgrade --no-cache-dir birdears``

In-depth installation
^^^^^^^^^^^^^^^^^^^^^

You can choose to use a virtualenv to use birdears; this should give you
an idea on how to setup one virtualenv.

You should first install virtualenv (for python3) using your
distribution’s package (supposing you’re on linux), then on terminal:

::

    virtualenv -p python3 venv # use the directory venv/ for the virtualenv
    venv/bin/activate # activate the virtualenv; this should be done every 
                      # time you may want to run the software installed here.
    pip install birdears # this will install it
    birdears --help # this will run it

