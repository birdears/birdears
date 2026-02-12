# The Functional Ear Training Method

`birdears` implements the **Functional Ear Training** method, which focuses on learning to recognize notes by their function (or degree) within a given musical key (tonality), rather than just identifying the interval distance between two isolated notes.

In this method, you learn to hear how each note relates to the **tonic** (the home note of the key). This builds a strong internal sense of tonality and allows you to transcribe melodies more naturally.

## How It Works

The core exercise typically follows this sequence:

1.  **Establish the Key**: A cadence is played to firmly anchor the key center in your ear. We recommend starting with the **I-IV-V-I** progression. While this specific cadence isn't the only standard, it's a powerful and clear way for beginners to lock into the tonality.
2.  **Play a Note**: A random note from the scale is played.
3.  **Identify**: You must identify the note's degree (e.g., "Third", "Fifth", "Major Seventh") or name relative to the key.
4.  **Resolution**: To reinforce the sound, the note is then resolved to the nearest stable tone (the tonic).

### Resolution Logic

To help internalize the sound, `birdears` automatically resolves the played note to the nearest stable tonic. This resolution helps you "feel" the gravity of each note—its pull towards home.

Here's how the magic happens:

-   **From I to IV (Unison to Perfect 4th)**: These notes feel a gravitational pull **downward** and resolve to the **Tonic (I)**.
    -   *Think of it as*: Falling back to the ground. An F (IV) naturally settles down to C (I).
-   **From V to VIII (Perfect 5th to Octave)**: These notes feel a lift **upward** and resolve to the **Octave (VIII)**.
    -   *Think of it as*: Reaching for the sky. A G (V) yearns to climb up to the high C (VIII).
-   **The Tritone**: This ambiguous interval (Augmented 4th / Diminished 5th) is currently resolved **up** to the octave, adding a touch of suspense before the release.

By hearing these resolutions repeatedly, you learn to anticipate where a note "wants to go," which is the essence of functional hearing.

## Modes

`birdears` offers several modes to practice different aspects of ear training:

-   **Melodic Interval**: Two notes are played sequentially. You identify the interval between them. (This is traditional interval training).
-   **Harmonic Interval**: Two notes are played simultaneously. You identify the interval.
-   **Melodic Dictation**: A sequence of notes (melody) is played. You must identify all the intervals or notes.
-   **Instrumental**: Similar to dictation, but you play the notes back on your instrument. `birdears` waits for you to confirm you've played it (it doesn't listen to you, it relies on your honor system!).
-   **Note Name**: This is the primary **Functional Ear Training** mode. A key is established, and you must identify the note names (e.g., C, D, E) or degrees within that context.
