import pytest
from birdears import INTERVALS
from birdears.interval import get_interval_by_semitones

def test_get_interval_by_semitones_valid_positive():
    # Test 0 semitones (Unison)
    interval = get_interval_by_semitones(0)
    assert interval == INTERVALS[0]
    assert interval[1] == 'P1'

    # Test 1 semitone (Minor Second)
    interval = get_interval_by_semitones(1)
    assert interval == INTERVALS[1]
    assert interval[1] == 'm2'

    # Test 12 semitones (Perfect Octave)
    interval = get_interval_by_semitones(12)
    assert interval == INTERVALS[12]
    assert interval[1] == 'P8'

    # Test max semitones (36)
    interval = get_interval_by_semitones(36)
    assert interval == INTERVALS[36]

def test_get_interval_by_semitones_valid_negative():
    # Test -1 semitone (should return same as 1)
    interval = get_interval_by_semitones(-1)
    assert interval == INTERVALS[1]

    # Test -12 semitones
    interval = get_interval_by_semitones(-12)
    assert interval == INTERVALS[12]

def test_get_interval_by_semitones_out_of_bounds():
    # Test > 36
    with pytest.raises(IndexError):
        get_interval_by_semitones(37)

    # Test < -36
    with pytest.raises(IndexError):
        get_interval_by_semitones(-37)
