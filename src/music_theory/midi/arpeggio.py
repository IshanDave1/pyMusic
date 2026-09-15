"""
Arpeggio generation utilities for fast chord arpeggiation.

Generates fast arpeggiated chord progressions with customizable patterns and spanning.
"""

from pathlib import Path
from midiutil import MIDIFile
from src.music_theory.core.notes import note_string_to_midi
from src.music_theory.core.chord import build_arpeggio_from_chord
from src.music_theory.core.constants import chords as CHORD_DEFINITIONS, interval_half_steps


def _get_chord_intervals(chord_type):
    """Convert chord type to semitone intervals."""
    if chord_type not in CHORD_DEFINITIONS:
        return [0, 4, 7]
    
    interval_names = CHORD_DEFINITIONS[chord_type]
    return [interval_half_steps.get(name, 0) for name in interval_names]


def generate_arpeggio_progression(chords, output_file=None, tempo=400, volume=60, 
                                   octaves_to_span=4, finger_pattern=None, verbose=False):
    """
    Generate fast arpeggiated chords.
    
    Args:
        chords: List of (base_note, chord_type) tuples
                e.g., [("D2", "minor_ninth"), ("G2", "dominant_ninth"), ...]
        output_file: Path to save MIDI file. If None, returns MIDIFile object.
        tempo: Tempo in BPM (default 400)
        volume: MIDI volume 0-127 (default 60)
        octaves_to_span: Number of octaves to span (default 4)
        finger_pattern: Optional list of pattern indices (e.g., [1, 2, 4, 3, 1, 2, 3, 4])
        verbose: Print debug info (default False)
    
    Returns:
        None if output_file is specified, otherwise MIDIFile object.
        Note: Each note in the arpeggio lasts 0.5 quarter notes.
    """
    
    midi = MIDIFile(1)
    midi.addTempo(0, 0, tempo)
    
    if finger_pattern is None:
        arpeggio_length = octaves_to_span * 8
    else:
        arpeggio_length = octaves_to_span * len(finger_pattern)
    
    if finger_pattern is None:
        finger_pattern = [1, 2, 4, 5, 2, 4, 6, 8]
    
    current_time = 0
    beat_duration = 0.5
    
    for base_note_str, chord_type_str in chords:
        base_midi = note_string_to_midi(base_note_str)
        intervals = _get_chord_intervals(chord_type_str)
        
        chord = [base_midi + interval for interval in intervals]
        arpeggio_notes = build_arpeggio_from_chord(chord, arpeggio_length, finger_pattern)
        
        for midi_note in arpeggio_notes:
            midi.addNote(0, 0, midi_note, current_time, beat_duration, volume)
            current_time += beat_duration
    
    if output_file is not None:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "wb") as f:
            midi.writeFile(f)
        if verbose:
            print(f"  Wrote: {output_file}")
        return None
    else:
        return midi
