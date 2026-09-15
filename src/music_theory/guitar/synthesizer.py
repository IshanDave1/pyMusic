"""
Guitar synthesizer for generating realistic strumming patterns from tablature.

Provides realistic guitar MIDI synthesis with configurable strum patterns,
velocity dynamics, string dropping, and strumming speed control.
"""

import random
from pathlib import Path
from midiutil import MIDIFile
from src.music_theory.guitar.guitar_chord import get_chord_from_tabs


class GuitarChordPattern:
    """Represents a guitar chord with tablature, duration, and strum pattern."""
    
    def __init__(self, tabs: list, chord_duration: float, pattern: list):
        """
        Initialize a guitar chord pattern.
        
        Args:
            tabs: Guitar tablature (fret positions for each string, -1 = not played).
            chord_duration: Duration in beats for this chord.
            pattern: Strum pattern (sequence of durations or weights).
        """
        self.tabs = tabs
        self.chord_duration = chord_duration
        self.pattern = pattern

    def __str__(self) -> str:
        return f"GuitarChordPattern(duration={self.chord_duration}, pattern={self.pattern}, tabs={self.tabs})"

    def __repr__(self) -> str:
        return self.__str__()


def calculate_string_delay(string_index: int, total_strings: int, tempo: int, base_strum_speed: float = 1.0) -> float:
    """Calculate delay time for each string in the strum to create natural spacing."""
    power_factor = 1.2
    normalized_position = string_index / total_strings
    base_delay = 0.05 * (30 / tempo)
    return base_delay * ((normalized_position) ** power_factor) / base_strum_speed


def calculate_note_time_in_pattern(pattern_progress: float, pattern_length: int, 
                                   chord_duration: float, total_duration: float,
                                   loop_index: int, chord_index: int, 
                                   chord_durations: list) -> float:
    """Calculate the absolute time for a note within the overall timing structure."""
    loop_time = loop_index * total_duration
    chord_start_time = sum(chord_durations[:chord_index])
    pattern_time = (chord_duration * pattern_progress) / pattern_length
    return loop_time + chord_start_time + pattern_time


def calculate_velocity_for_string(string_index: int, total_strings: int, base_volume: int, is_first_string: bool = False) -> int:
    """Calculate velocity (volume) for a string based on its position in the strum."""
    if is_first_string:
        return base_volume // 2
    return max(0, base_volume - 5 * string_index)


def should_drop_string(string_index: int, drop_probability: float = 0.0) -> bool:
    """Randomly determine if a string should be skipped in the strum."""
    if drop_probability <= 0:
        return False
    return random.random() < drop_probability


def synthesize_guitar_progression(
    chord_patterns: list,
    num_loops: int = 4,
    string_drop_probability: float = 0.0,
    base_strum_speed: float = 1.0,
    tempo: int = 90,
    base_volume: int = 70,
    output_path: str = None,
    verbose: bool = False
):
    """
    Generate MIDI for guitar chord progression with strumming patterns.
    
    Args:
        chord_patterns: List of GuitarChordPattern objects.
        num_loops: Number of times to repeat the chord progression.
        string_drop_probability: Probability of randomly skipping strings (0-1).
        base_strum_speed: Speed multiplier for strumming (1.0 = normal).
        tempo: Tempo in BPM.
        base_volume: Base MIDI volume (0-127).
        output_path: Path to save MIDI file. If None, returns MIDIFile object.
        verbose: Print debug info.
    
    Returns:
        None if output_path specified, otherwise MIDIFile object.
    """
    
    MIDI_TRACK = 0
    MIDI_CHANNEL = 0
    START_TIME = 0
    BASE_NOTE_DURATION = 0.08 * 4
    
    midi = MIDIFile(1)
    midi.addTempo(MIDI_TRACK, START_TIME, tempo)
    
    total_duration = sum(cp.chord_duration for cp in chord_patterns)
    
    for loop_idx in range(num_loops):
        for chord_idx, chord_pattern in enumerate(chord_patterns):
            pattern_length = sum(chord_pattern.pattern)
            
            for pattern_step, pattern_value in enumerate(chord_pattern.pattern):
                is_strumming_down = (sum(chord_pattern.pattern[:pattern_step]) % 2 == 0)
                
                chord_notes = get_chord_from_tabs(chord_pattern.tabs)
                if not is_strumming_down:
                    chord_notes = chord_notes[::-1]
                
                for string_idx, note in enumerate(chord_notes):
                    if should_drop_string(string_idx, string_drop_probability):
                        continue
                    
                    pattern_progress = sum(chord_pattern.pattern[:pattern_step])
                    note_time = calculate_note_time_in_pattern(
                        pattern_progress,
                        pattern_length,
                        chord_pattern.chord_duration,
                        total_duration,
                        loop_idx,
                        chord_idx,
                        [cp.chord_duration for cp in chord_patterns]
                    )
                    
                    string_delay = calculate_string_delay(
                        string_idx,
                        len(chord_notes),
                        tempo,
                        base_strum_speed
                    )
                    
                    final_time = note_time + string_delay
                    
                    is_first_string = (string_idx == 0)
                    velocity = calculate_velocity_for_string(
                        string_idx,
                        len(chord_notes),
                        base_volume,
                        is_first_string
                    )
                    
                    midi.addNote(
                        MIDI_TRACK,
                        MIDI_CHANNEL,
                        note,
                        final_time,
                        BASE_NOTE_DURATION,
                        velocity
                    )
    
    if output_path is not None:
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            midi.writeFile(f)
        if verbose:
            print(f"  Wrote: {output_path}")
        return None
    else:
        return midi
