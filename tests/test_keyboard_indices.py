
import pytest
from birdears import KEYBOARD_INDICES

def parse_intervals(key_string):
    """Parses a keyboard string into a list of semitone intervals."""
    intervals = []
    accum = 0
    # Skip the first key, start checking intervals from there
    # But strings start with a key.
    # We need to iterate from the second character?
    # No, iterate all chars, track state.

    # We assume valid string starts with a key
    if not key_string:
        return []

    # Check first char is not space
    if key_string[0] == ' ':
        raise ValueError("String starts with space")

    # Start loop from second char
    # We need to track if we are 'inside' a key sequence

    last_was_space = False

    # Actually, simplistic parser:
    # Key -> Key : 1 semitone
    # Key -> Space -> Key : 2 semitones
    # Key -> Space -> Space -> Key : 3 semitones (unlikely but possible)

    # We just need to count steps between keys.
    # We can filter out spaces and count indices? No.
    # We can iterate and count.

    current_interval = 1
    # Logic:
    # When we see a key, we record the interval from the PREVIOUS key.
    # But we need to handle the first key.

    keys_chars = []

    # Sanitize string to list of tokens?
    # "z x" -> z, space, x

    # Let's iterate index 1 to len

    extracted_intervals = []

    # Check if first char is key
    if key_string[0] == ' ':
        return []

    space_count = 0

    for char in key_string[1:]:
        if char == ' ':
            space_count += 1
        else:
            # It is a key
            interval = 1 + space_count
            extracted_intervals.append(interval)
            space_count = 0

    return extracted_intervals

def test_descending_diatonic_major():
    # Major Scale Descending Intervals: H, W, W, W, H, W, W
    # [1, 2, 2, 2, 1, 2, 2]
    # We expect 2 octaves.
    expected_intervals = [1, 2, 2, 2, 1, 2, 2] * 2

    # Get the string from __init__.py (after we fix it, but currently it's wrong)
    # Wait, if I write the test BEFORE fixing, it will fail.
    # That is good TDD.

    key_string = KEYBOARD_INDICES['diatonic']['descending']['major']

    # We expect this to fail currently because the string is a copy of ascending
    # Ascending Major (reversed logic? No, just copied)
    # Copied Ascending: z x cv b n mZ X CV B NM,
    # Let's see what intervals this parses to.
    # z->x (W), x->c (W), c->v (H)...
    # [2, 2, 1, 2, 2, 2, 1] ...
    # So it parses to Ascending intervals.
    # But we want Descending intervals [1, 2, 2, 2, 1, 2, 2]

    intervals = parse_intervals(key_string)

    assert intervals == expected_intervals

def test_descending_diatonic_minor():
    # Natural Minor Descending Intervals: W, W, H, W, W, H, W
    # [2, 2, 1, 2, 2, 1, 2]
    expected_intervals = [2, 2, 1, 2, 2, 1, 2] * 2

    key_string = KEYBOARD_INDICES['diatonic']['descending']['minor']

    intervals = parse_intervals(key_string)

    assert intervals == expected_intervals
