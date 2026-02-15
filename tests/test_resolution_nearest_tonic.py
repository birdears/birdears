
import pytest
from birdears.questions.melodicdictation import MelodicDictationQuestion
from birdears.questions.melodicinterval import MelodicIntervalQuestion
from birdears.resolution import nearest_tonic
from birdears.sequence import Sequence
from birdears.note_and_pitch import Pitch, Chord

def test_nearest_tonic_multiple_pitches():
    """
    Test nearest_tonic resolution with MelodicDictationQuestion which uses random_pitches.
    """
    # Create a question with random_pitches
    q = MelodicDictationQuestion(resolution_method='nearest_tonic', n_notes=3)

    # Resolve
    res_sequence = nearest_tonic(q)

    assert isinstance(res_sequence, Sequence)
    # Check that sequence is not empty
    assert len(res_sequence) > 0

    # Verify elements are Pitches or Chords
    for elem in res_sequence:
        assert isinstance(elem, (Pitch, Chord))

def test_nearest_tonic_single_pitch():
    """
    Test nearest_tonic resolution with MelodicIntervalQuestion which uses random_pitch.
    Regression test to ensure single pitch resolution still works.
    """
    q = MelodicIntervalQuestion(resolution_method='nearest_tonic')

    res_sequence = nearest_tonic(q)

    assert isinstance(res_sequence, Sequence)
    assert len(res_sequence) > 0

    for elem in res_sequence:
        assert isinstance(elem, (Pitch, Chord))

def test_nearest_tonic_chromatic_pitch():
    """
    Test resolution of a chromatic pitch to ensure it's handled correctly.
    """
    # Force a chromatic pitch
    # Using MelodicIntervalQuestion and manually setting random_pitch to something chromatic relative to C Major
    q = MelodicIntervalQuestion(tonic='C', mode='major', octave=4)
    # C#4 is chromatic in C Major
    q.random_pitch = Pitch(note='C#', octave=4)

    res_sequence = nearest_tonic(q)

    # Should resolve C# -> D -> C (or C# -> C depending on logic)
    # C# is semitone 1. Tonic is 0. Diff is 1.
    # Logic: semitones=1 <= MAX_SEMITONES_RESOLVE_BELOW(5). direction=-1.
    # nearest_diatonic = C# - 1 = C.
    # nearest_tonic = C.
    # Resolution should be [C#, C].

    elements = list(res_sequence)
    # Check that the first element is our chromatic pitch (or close to it)
    # The current logic inserts random_pitch at start if chromatic.
    assert elements[0] == q.random_pitch

    # Check that it resolves to tonic
    assert elements[-1] == q.tonic_pitch
