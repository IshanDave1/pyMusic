"""Core music theory modules: notes, chords, and scales."""

from src.music_theory.core.chord import ChordEvent
from src.music_theory.core.constants import chords, interval_half_steps, notes, scales
from src.music_theory.core.notes import (
    build_chord,
    build_diatonic_chord,
    build_scale_midi,
    build_scale_note_strings,
    midi_to_note_string,
    note_string_to_midi,
    note_to_midi,
    parse_chord_token,
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
    "parse_chord_token",
    "ChordEvent",
    "build_diatonic_chord",
    "transpose_note_to_string",
    "transpose_to_midi",
]
