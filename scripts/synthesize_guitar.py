#!/usr/bin/env python3
"""
Simple Guitar Synthesizer
Just edit the inputs below and run: python synthesize_guitar.py
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import from src/
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.music_theory.guitar.synthesizer import synthesize_guitar_progression, GuitarChordPattern

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES
# ============================================================================

# Guitar chords (tabs format: -1 = not played, 0-12 = fret position)
# STANDARD TUNING: E2, A2, D3, G3, B3, E4
GUITAR_CHORDS = [
    [-1, 0, 2, 2, 1, 0],      # Em7
    [3, 2, 0, 0, 0, 3],        # F#m7
    [-1, -1, 0, 2, 3, 2],      # A (barre)
    [-1, -1, 0, 2, 3, 2],      # A (barre)
]

# Chord duration in quarter notes
# (At 90 BPM: 4 quarter notes = 1 whole note = 2.67 seconds)
CHORD_DURATION = 4

# Strum pattern (higher values = longer notes sound)
STRUM_PATTERN = [3, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1]

# Output file path
OUTPUT_FILE = "../outputs/my_guitar.mid"

# Tempo in BPM
TEMPO = 90

# Volume (0-127)
VOLUME = 70

# Number of loops (repetitions of the chord progression)
LOOPS = 3

# Probability of skipping strings (0.0 = never, 1.0 = always)
DROP_PROBABILITY = 0.15

# Strum speed multiplier (1.0 = normal, 0.5 = slow, 2.0 = fast)
STRUM_SPEED = 1.0

# Random seed for reproducibility (None = random each time)
SEED = 42

# ============================================================================
# GENERATE
# ============================================================================

if __name__ == "__main__":
    import random
    if SEED is not None:
        random.seed(SEED)
    
    print(f"Generating guitar synthesis...")
    print(f"  Chords: {len(GUITAR_CHORDS)}")
    print(f"  Tempo: {TEMPO} BPM")
    print(f"  Volume: {VOLUME}")
    print(f"  Loops: {LOOPS}")
    print(f"  String drop probability: {DROP_PROBABILITY * 100:.1f}%")
    print(f"  Strum speed: {STRUM_SPEED}x")
    
    # Create chord patterns
    chord_patterns = []
    for tabs in GUITAR_CHORDS:
        chord_patterns.append(GuitarChordPattern(tabs, CHORD_DURATION, STRUM_PATTERN))
    
    # Generate
    synthesize_guitar_progression(
        chord_patterns=chord_patterns,
        num_loops=LOOPS,
        string_drop_probability=DROP_PROBABILITY,
        base_strum_speed=STRUM_SPEED,
        tempo=TEMPO,
        base_volume=VOLUME,
        output_path=OUTPUT_FILE,
        verbose=True,
    )
    
    print(f"\n✓ Done! Check: {OUTPUT_FILE}")
