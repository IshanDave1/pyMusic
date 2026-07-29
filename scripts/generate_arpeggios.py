#!/usr/bin/env python3
"""
Simple Arpeggio Generator
Just edit the inputs below and run: python generate_arpeggios.py
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import from src/
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.music_theory.midi.arpeggio import generate_arpeggio_progression

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES
# ============================================================================

# Chords: List of (base_note, chord_type) tuples
CHORDS = [
    ("D2", "minor_ninth"),
    ("G2", "dominant_ninth"),
    ("C2", "major_ninth"),
    ("A2", "minor_ninth"),
]

# Output file path
OUTPUT_FILE = "../outputs/my_arpeggios.mid"

# Tempo in BPM
TEMPO = 400

# Volume (0-127)
VOLUME = 60

# Number of octaves to span
OCTAVES = 4

# Finger pattern (which notes to play)
# None = default [0, 2, 4, 5, 2, 4, 6, 8]
# Or specify your own: [0, 1, 2, 3, 4, 5]
FINGER_PATTERN = None

# ============================================================================
# GENERATE
# ============================================================================

if __name__ == "__main__":
    print(f"Generating arpeggio progression...")
    print(f"  Chords: {CHORDS}")
    print(f"  Tempo: {TEMPO} BPM")
    print(f"  Volume: {VOLUME}")
    print(f"  Octaves: {OCTAVES}")
    
    generate_arpeggio_progression(
        CHORDS,
        output_file=OUTPUT_FILE,
        tempo=TEMPO,
        volume=VOLUME,
        octaves_to_span=OCTAVES,
        finger_pattern=FINGER_PATTERN,
        verbose=True,
    )
    
    print(f"\n✓ Done! Check: {OUTPUT_FILE}")
