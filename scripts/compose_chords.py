#!/usr/bin/env python3
"""
Simple Chord Progression Generator
Just edit the inputs below and run: python compose_chords.py
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import from src/
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.music_theory.core.chord import ChordEvent
from src.music_theory.midi.compose import compose_chord_progression

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES
# ============================================================================

# Output file path
OUTPUT_FILE = "../outputs/my_chords.mid"

# Tempo in BPM
TEMPO = 120

# Volume (0-127)
VOLUME = 50

# Enable smooth voicing (minimal note movement between chords and across sections)
SMOOTH_VOICING = True

# ============================================================================
# SECTIONS - Define chord progressions with their durations, patterns, and loops
# ============================================================================
# Chord format: "ROOT[:QUALITY]"; omitted quality means major.
# Use ChordEvent for per-chord voicing options.

SECTIONS = [
    (
        [
            "A",
            "Fs:m",
            "Gs:sus4",
        ],
        [4, 4, 4],
        [2, 2, 1, 2, 2, 1, 2, 4],
        2,
    ),
    (
        [
            "Ds:m",
            "B",
            "Cs",
            "Fs",
            "Ds:m",
            "B",
            "Cs",
            "Fs",
            "Ds:m",
            "B",
            "Cs",
            "Fs",
            "Ds:m",
            "B",
            "Cs",
            "Cs:sus4",
        ],
        [4] * 16,
        [1],
        1,
    ),
]

DOUBLED = {"lower_octave_doubles": (0, 1, 2)}

for section_idx, (chords, durations, patterns, loops) in enumerate(SECTIONS):
    new_chords = []
    for chord in chords:
        if isinstance(chord, ChordEvent):
            new_chords.append(
                ChordEvent(
                    chord=chord.chord,
                    inversion=chord.inversion,
                    lower_octave_doubles=DOUBLED["lower_octave_doubles"],
                    upper_octave_doubles=chord.upper_octave_doubles,
                    over_octaves=chord.over_octaves,
                    openness=chord.openness,
                    rootless=chord.rootless,
                )
            )
        else:
            new_chords.append(ChordEvent(chord=chord, **DOUBLED))

    SECTIONS[section_idx] = (new_chords, durations, patterns, loops)


if __name__ == "__main__":
    print(f"Generating {len(SECTIONS)} chord progression section(s)...")
    print(f"  Tempo: {TEMPO} BPM")
    print(f"  Volume: {VOLUME}")
    print(f"  Smooth voicing: {SMOOTH_VOICING}")

    for i, section in enumerate(SECTIONS, 1):
        chords, chord_durations, pattern, loop_count = section
        print(f"\n  Section {i}:")
        print(f"    Chords: {len(chords)} chords")
        print(f"    Durations: {chord_durations}")
        print(f"    Loops: {loop_count}")

    compose_chord_progression(
        SECTIONS,
        output_file=OUTPUT_FILE,
        tempo=TEMPO,
        volume=VOLUME,
        smooth_voicing=True,
        verbose=True,
    )

    print(f"\n✓ Done! Check: {OUTPUT_FILE}")
