import pytest
from birdears.note_and_pitch import get_pitch_class, CHROMATIC_SHARP, CHROMATIC_FLAT
from birdears.exception import InvalidNote

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
