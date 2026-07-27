"""Core music theory modules: notes, chords, and scales."""

from src.music_theory.core.constants import notes, scales, chords, interval_half_steps
from src.music_theory.core.notes import (
    note_to_midi,
    note_string_to_midi,
    midi_to_note_string,
    build_scale_midi,
    build_scale_note_strings,
    build_chord,
    build_diatonic_chord,
    transpose_note_to_string,
    transpose_to_midi,
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
    "build_scale_note_strings",
    "build_chord",
    "build_diatonic_chord",
    "transpose_note_to_string",
    "transpose_to_midi",
]
