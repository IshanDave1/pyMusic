"""MIDI composition and synthesis utilities."""

from src.music_theory.midi.compose import compose_chord_progression
from src.music_theory.midi.arpeggio import generate_arpeggio_progression

__all__ = ["compose_chord_progression", "generate_arpeggio_progression"]
