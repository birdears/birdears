# Fix Explanation: Descending Keys for Diatonic Modes

The original implementation of descending keys for diatonic modes in `src/birdears/__init__.py` was marked with `# FIXME` and contained strings that were exact copies of the ascending keys. This was incorrect for several reasons:

1.  **Directionality**: A descending scale should start from the highest pitch (key `,` on the mapping) and move to the lowest pitch (`z`). The original strings started with `z` (lowest key), representing an ascending movement.
2.  **Interval Sequence**:
    *   **Major Scale (Ascending)**: W-W-H-W-W-W-H (e.g., C-D-E-F-G-A-B-C).
    *   **Major Scale (Descending)**: The intervals are reversed: H-W-W-W-H-W-W (e.g., C-B-A-G-F-E-D-C).
    *   **Natural Minor Scale (Ascending)**: W-H-W-W-H-W-W (e.g., A-B-C-D-E-F-G-A).
    *   **Natural Minor Scale (Descending)**: The intervals are reversed: W-W-H-W-W-H-W (e.g., A-G-F-E-D-C-B-A).

The copied strings in the original code preserved the ascending interval structure (W-W-H... for Major, W-H-W... for Minor), which is incorrect for a descending scale.

**The Fix:**
I replaced the incorrect strings with sequences that:
1.  Start from `,` and descend to `z`.
2.  Reflect the correct descending interval patterns by adjusting the spacing (spaces represent whole steps, adjacent characters represent half steps).

*   **New Major Descending**: `,M N B VC X Zm n b vc x z` (H-W-W-W-H-W-W)
*   **New Minor Descending**: `, M NB V CX Z m nb v cx z` (W-W-H-W-W-H-W)

A regression test `tests/test_keyboard_indices.py` was added to verify these interval sequences programmatically.
