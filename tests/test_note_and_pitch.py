import pytest

from birdears.note_and_pitch import get_pitch_class, CHROMATIC_SHARP, CHROMATIC_FLAT
from birdears.exception import InvalidNote
from birdears.note_and_pitch import Note, Pitch, Chord, get_pitch_by_number, get_abs_chromatic_offset, get_pitch_number, get_pitch_class
from birdears.exception import InvalidNote, InvalidOctave, InvalidPitch

def test_get_pitch_class_sharp():
    for index, note in enumerate(CHROMATIC_SHARP):
        assert get_pitch_class(note) == index

def test_get_pitch_class_flat():
    for index, note in enumerate(CHROMATIC_FLAT):
        assert get_pitch_class(note) == index

def test_get_pitch_class_invalid():
    invalid_notes = ['H', 'I', 'Z', 'C#b', 'Db#', '', 123, None]
    for note in invalid_notes:
        with pytest.raises(InvalidNote):
            get_pitch_class(note)


def test_get_pitch_class():
    assert get_pitch_class('C') == 0
    assert get_pitch_class('Db') == 1
    with pytest.raises(InvalidNote):
        get_pitch_class('H')

def test_get_pitch_number():
    assert get_pitch_number('C', 4) == 48
    assert get_pitch_number('C', 0) == 0

def test_note_init():
    n = Note('C')
    assert n.note == 'C'
    assert n.accident == 'sharp' # Default

    n = Note('Db')
    assert n.note == 'Db'

    with pytest.raises(InvalidNote):
        Note('H')

def test_note_comparison():
    n1 = Note('C')
    n2 = Note('C')
    assert n1 == n2

    # Note vs String
    assert n1 == 'C'
    assert n1 != 'D'

    # Note vs Pitch
    # int(Note) returns pitch_class (0-11)
    # int(Pitch) returns pitch_number (0-127)

    p = Pitch('C', 4) # 48
    # 0 != 48
    assert n1 != p

    p0 = Pitch('C', 0) # 0
    # 0 == 0
    assert n1 == p0

def test_pitch_init():
    p = Pitch('C', 4)
    assert p.note == 'C'
    assert p.octave == 4
    assert p.pitch_number == 48 # 4 * 12 + 0

    with pytest.raises(InvalidOctave):
        Pitch('C', 10) # Max is 9

    with pytest.raises(InvalidOctave):
        Pitch('C', -1)

def test_pitch_arithmetic():
    p = Pitch('C', 4) # 48

    # Add int
    p2 = p + 2 # D4 (50)
    assert p2.note == 'D'
    assert p2.octave == 4

    p3 = p + 12 # C5 (60)
    assert p3.note == 'C'
    assert p3.octave == 5

    # Sub int
    p4 = p3 - 12
    assert p4 == p

    # In-place add/sub
    p5 = Pitch('C', 4)
    p5 += 2
    assert p5.note == 'D'

    p6 = Pitch('D', 4)
    p6 -= 2
    assert p6.note == 'C'

def test_pitch_comparison():
    p1 = Pitch('C', 4)
    p2 = Pitch('D', 4)

    assert p1 < p2
    assert p2 > p1
    assert p1 <= p2
    assert p1 <= p1
    assert p1 != p2
    assert p1 == 48

    # Comparison with int
    assert p1 == 48
    assert p1 < 49
    assert p1 > 47

    with pytest.raises(Exception):
        p1 == "string"

def test_pitch_distance():
    p1 = Pitch('C', 4) # 48
    p2 = Pitch('D', 4) # 50

    assert p1.distance(p2) == -2
    assert p2.distance(p1) == 2
    assert p1.distance(48) == 0

def test_get_pitch_by_number():
    p = get_pitch_by_number(60) # C5
    assert p.note == 'C'
    assert p.octave == 5

    p = get_pitch_by_number(61, accident='flat') # Db5
    assert p.note == 'Db'
    assert p.octave == 5

def test_chord():
    p1 = Pitch('C', 4)
    p2 = Pitch('E', 4)
    p3 = Pitch('G', 4)

    c = Chord([p1, p2, p3])
    assert len(c) == 3

    with pytest.raises(InvalidPitch):
        Chord([p1, 'not a pitch'])

    c.append(Pitch('C', 5))
    assert len(c) == 4

    with pytest.raises(InvalidPitch):
        c.append('invalid')

    c.extend([Pitch('E', 5)])
    assert len(c) == 5

    with pytest.raises(InvalidPitch):
        c.extend(['invalid'])

def test_get_abs_chromatic_offset():
    p1 = Pitch('C', 4)
    p2 = Pitch('G', 4)

    offset = get_abs_chromatic_offset(p1, p2)
    assert offset == 7 # 7 semitones

    # Test modulo 12
    p3 = Pitch('C', 5)
    offset2 = get_abs_chromatic_offset(p1, p3)
    assert offset2 == 0 # 12 % 12 == 0

