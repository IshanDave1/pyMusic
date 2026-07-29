#!/usr/bin/env python3
"""
Simple Chord Progression Generator
Just edit the inputs below and run: python compose_chords.py
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import from src/
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.music_theory.midi.compose import compose_chord_progression

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES
# ============================================================================

# Chords: List of (base_note, chord_type) tuples with optional inversion/voicing
# Supports multiple formats:
#   ("Gs3", "minor")                    - simple
#   ("Gs3", "minor", 1)                 - with inversion
#   ("Gs3", "minor", {"inversion": 1})  - with voicing options (dict)
#   ("Gs3", "minor", 1, {"openness": 0.3})  - mixed: inversion + voicing dict


# Output file path
OUTPUT_FILE = "../outputs/my_chords.mid"

# Tempo in BPM
TEMPO = 80

# Volume (0-127)
VOLUME = 70

# Enable smooth voicing (minimal note movement between chords)
SMOOTH_VOICING = True

SECTIONS = []
CHORDS = [
    ("C", "major_ninth"),     # Approximation of G/C (closest in your library)
    ("B", "minor_seventh"),   # D/B (same notes)
    ("A", "major"),
    ("A", "sus4"),
    ("A", "major"),
]

# Duration of each chord in quarter notes
CHORD_DURATIONS = [4, 4,4,2,2]

# Pattern for how many times to play the entire chord during its duration
PATTERN = [[1,1],[1,1],[1,1],[1],[1]]

# Number of times to loop the entire chord progression
LOOP_COUNT = 3
SECTIONS.append((CHORDS,CHORD_DURATIONS,PATTERN,LOOP_COUNT))

print(SECTIONS)



# ============================================================================
# GENERATE
# ============================================================================

if __name__ == "__main__":
    print(f"Generating chord progression...")
    print(f"  Chords: {CHORDS}")
    print(f"  Tempo: {TEMPO} BPM")
    print(f"  Volume: {VOLUME}")
    print(f"  Chord durations: {CHORD_DURATIONS} quarter notes")
    if PATTERN:
        print(f"  Pattern: {PATTERN}")
    print(f"  Loops: {LOOP_COUNT}")
    print(f"  Smooth voicing: {SMOOTH_VOICING}")
    
    compose_chord_progression(
        CHORDS,
        output_file=OUTPUT_FILE,
        tempo=TEMPO,
        volume=VOLUME,
        chord_durations=CHORD_DURATIONS,
        patterns=PATTERN,
        loop_count=LOOP_COUNT,
        smooth_voicing=SMOOTH_VOICING,
        verbose=True,
    )
    
    print(f"\n✓ Done! Check: {OUTPUT_FILE}")
