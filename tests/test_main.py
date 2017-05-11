from unittest import mock

from birdears import __main__

def test_cli(monkeypatch):

    from birdears.__main__ import cli
    sys_argv = ['PYTEST_ARGV0', '--help']
    monkeypatch.setattr('sys.argv', sys_argv)

    try:
        a = cli()
    except SystemExit:
        pass

    assert(True)

def test_cli_melodic(monkeypatch):

    from birdears.__main__ import melodic
    def mockreturn():
        return lambda: 'q' # quits

    sys_argv = ['PYTEST_ARGV0', 'melodic']

    monkeypatch.setattr('birdears.__main__._Getch', mockreturn)
    monkeypatch.setattr('sys.argv', sys_argv)

    try:
        a = __main__.cli()
    except SystemExit:
        pass

    assert(True)

def test_cli_harmonic(monkeypatch):

    from birdears.__main__ import harmonic
    def mockreturn():
        return lambda: 'q' # quits

    sys_argv = ['PYTEST_ARGV0', 'harmonic']

    monkeypatch.setattr('sys.argv', sys_argv)
    monkeypatch.setattr('birdears.__main__._Getch', mockreturn)

    try:
        a = __main__.cli()
    except SystemExit:
        pass

    assert(True)

def test_cli_dictation(monkeypatch):

    def mockreturn():
        return lambda: 'q' # quits

    sys_argv = ['PYTEST_ARGV0', 'dictation']

    monkeypatch.setattr('sys.argv', sys_argv)
    monkeypatch.setattr('birdears.__main__._Getch', mockreturn)

    try:
        a = __main__.cli()
    except SystemExit:
        pass

    assert(True)
