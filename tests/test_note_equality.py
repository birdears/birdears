from birdears.note_and_pitch import Note, Pitch

def test_note_equality():
    n = Note('C')
    assert n == 'C'
    assert n != 'D'
    assert n == Note('C')
    assert n != Note('D')

    # Pitch equality behavior
    # n is C (pitch class 0)
    # p is C4 (pitch number 48)
    p = Pitch('C', 4)
    # n == p: Note.__eq__(p) -> isinstance(p, Note) -> int(n)=0 == int(p)=48 -> False.
    assert n != p

    # p0 is C0 (pitch number 0)
    p0 = Pitch('C', 0)
    # n == p0: Note.__eq__(p0) -> isinstance(p0, Note) -> int(n)=0 == int(p0)=0 -> True.
    assert n == p0

    # Test subclasses of str
    class MyString(str):
        pass

    ms = MyString('C')
    # With isinstance() check, this should be True.
    assert n == ms
