"""Music theory utilities for building scales, chords, and compositions."""

from src.music_theory.core.constants import notes, scales, chords, interval_half_steps
from src.music_theory.core.notes import (
    note_to_midi,
    note_string_to_midi,
    midi_to_note_string,
    build_scale_midi,
    build_chord,
)

__all__ = [
    "notes",
    "scales",
    "chords",
    "interval_half_steps",
    "note_to_midi",
    "note_string_to_midi",
    "midi_to_note_string",
    "build_scale_midi",
    "build_chord",
]
