"""Music theory utilities for building scales, chords, and compositions."""

from src.music_theory.core.chord import ChordEvent
from src.music_theory.core.constants import chords, interval_half_steps, notes, scales
from src.music_theory.core.notes import (
    build_chord,
    build_scale_midi,
    midi_to_note_string,
    note_string_to_midi,
    note_to_midi,
    parse_chord_token,
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
    "parse_chord_token",
    "ChordEvent",
]
