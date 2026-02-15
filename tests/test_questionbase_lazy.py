from birdears.questionbase import QuestionBase
from birdears.scale import ChromaticScale

def test_questionbase_lazy_chromatic_scale():
    # Case 1: chromatic=False (default)
    q = QuestionBase(chromatic=False)

    # Verify _chromatic_scale is None (lazy not yet triggered)
    assert q._chromatic_scale is None

    # Access property
    cs = q.chromatic_scale

    # Verify it is a ChromaticScale
    assert isinstance(cs, ChromaticScale)

    # Verify it is now cached
    assert q._chromatic_scale is not None
    assert q._chromatic_scale is cs

    # Verify consistency
    assert str(cs[0].note) == q.tonic_str

def test_questionbase_eager_chromatic_scale():
    # Case 2: chromatic=True
    q = QuestionBase(chromatic=True)

    # Verify _chromatic_scale is set (eager initialization as part of scale)
    assert q._chromatic_scale is not None

    # Verify it is the same as scale
    assert q._chromatic_scale is q.scale

    # Access property
    cs = q.chromatic_scale

    # Verify it is the same object
    assert cs is q.scale
