#!/usr/bin/env python3
"""
Simple Raga Melody Generator
Just edit the inputs below and run: python generate_raga.py
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import from src/
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.music_theory.raga.raga_generator import generate_raga_melody_prog

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES
# ============================================================================

# Length of melody in note indices
LENGTH = 256

# Output file path
OUTPUT_FILE = "../outputs/my_raga.mid"

# Tempo in BPM
TEMPO = 240

# Volume (0-127)
VOLUME = 80

# Beats per whole note (4 = standard 4/4 time)
BEAT_DURATION = 4

# ============================================================================
# GENERATE
# ============================================================================

if __name__ == "__main__":
    print(f"Generating raga melody...")
    print(f"  Length: {LENGTH} notes")
    print(f"  Tempo: {TEMPO} BPM")
    print(f"  Volume: {VOLUME}")
    print(f"  Beat duration: {BEAT_DURATION}")
    
    generate_raga_melody_prog(
        length=LENGTH,
        output_file=OUTPUT_FILE,
        tempo=TEMPO,
        volume=VOLUME,
        beat_duration=BEAT_DURATION,
        verbose=True,
    )
    
    print(f"\n✓ Done! Check: {OUTPUT_FILE}")
