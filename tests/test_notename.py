import pytest
from random import choice
from birdears import CHROMATIC_SHARP, CHROMATIC_FLAT, KEYBOARD_INDICES
from birdears.questions.notename import NoteNameQuestion

def test_notename_question_init():
    keys = list(CHROMATIC_SHARP)
    keys.extend(CHROMATIC_FLAT)

    mode = choice(['major', 'minor'])
    tonic = choice(keys)
    octave = choice([3, 4, 5])
    descending = choice([False, True])
    chromatic = choice([False, True])
    n_octaves = choice([1, 2])

    for i in range(20):
        q = NoteNameQuestion(mode=mode, tonic=tonic, octave=octave,
                             descending=descending, chromatic=chromatic,
                             n_octaves=n_octaves)
        assert q

def test_notename_flat_tonic():
    # Reproduces the bug with Db tonic
    # We need to force the random pitch to be something specific or test check_question generally
    # Here we just verify it doesn't crash when checking an answer

    q = NoteNameQuestion(tonic='Db', octave=4)
    # 'z' corresponds to Db in standard chromatic layout (tonic)

    # If the random pitch is Db, then 'z' is correct.
    # Regardless, it should not crash.
    response = q.check_question('z')

    assert response['user_note'] == 'Db'

    if q.random_pitch.note == 'Db':
        assert response['is_correct']

def test_check_question_correctness():
    # Test with C major
    q = NoteNameQuestion(tonic='C', octave=4)

    # We need to know what the correct answer is.
    # q.random_pitch is the correct note.
    correct_note = q.random_pitch.note

    # Find the key for this note.
    # C major chromatic ascending:
    # C C# D D# E F F# G G# A A# B
    # z s  x d  c v g  b h  n j  m

    mapping_indices = {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4,
        'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9,
        'A#': 10, 'Bb': 10, 'B': 11
    }

    # Using the string from source code to be safe
    keyboard_keys = "zsxdcvgbhnjm"

    semitones = mapping_indices[correct_note]
    correct_key = keyboard_keys[semitones]

    response = q.check_question(correct_key)
    assert response['is_correct']
    assert response['correct_note'] == correct_note

    # Test incorrect answer
    incorrect_semitones = (semitones + 1) % 12
    incorrect_key = keyboard_keys[incorrect_semitones]

    response = q.check_question(incorrect_key)
    assert not response['is_correct']
