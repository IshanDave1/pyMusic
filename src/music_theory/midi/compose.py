"""
Chord composition utilities for generating MIDI progressions.

Converts simple (note_string, chord_type) specifications into full MIDI chord progressions.
"""

from pathlib import Path
from midiutil import MIDIFile
from src.music_theory.core.notes import build_chord, find_chord_voicing_by_common_tones


def compose_chord_progression(chords, output_file=None, tempo=120, volume=70, 
                              chord_durations=None, patterns=None, loop_count=1, 
                              smooth_voicing=False, verbose=False):
    """
    Generate a chord progression from note/chord type pairs.
    
    Args:
        chords: List of chord specifications. Each can be:
                - (base_note, chord_type) - e.g., ("C4", "major")
                - (base_note, chord_type, inversion) - e.g., ("C4", "major", 1)
                - (base_note, chord_type, voicing_dict) - e.g., ("C4", "major", {"inversion": 1, "openness": 0.3})
                - (base_note, chord_type, inversion, voicing_dict) - mixed format
                
                Voicing options in dict: inversion, lower_octave_doubles, upper_octave_doubles, 
                                        over_octaves, openness, rootless
        output_file: Path to save MIDI file. If None, returns MIDIFile object.
        tempo: Tempo in BPM (default 120)
        volume: MIDI volume 0-127 (default 70)
        chord_durations: List of durations per chord in quarter notes (default [4] * len(chords)).
                        Each chord lasts this duration.
        patterns: List of relative timings for how many times to play each chord during its duration.
                 E.g., [3, 3, 2] means play the entire chord 3 times, then 3 times, then 2 times,
                 with timings 3/8, 3/8, 2/8 of the chord_duration respectively.
                 If None, equivalent to [1] - chord plays once for full duration.
        loop_count: Number of times to repeat the entire chord progression (default 1).
        smooth_voicing: If True, uses find_chord_voicing_by_common_tones() to smooth voice
                       leading between consecutive chords, minimizing note movement (default False).
        verbose: Print debug info (default False)
    
    Returns:
        None if output_file is specified, otherwise MIDIFile object
    """
    
    # Default durations
    if chord_durations is None:
        chord_durations = [4] * len(chords)
    
    midi = MIDIFile(1)
    midi.addTempo(0, 0, tempo)
    
    current_time = 0
    previous_chord_notes = None  # Track previous chord for smoothening
    
    # Loop the entire chord progression
    for loop_idx in range(loop_count):
        previous_chord_notes = None
        for chord_idx, chord_item in enumerate(chords):
            # Parse chord item - supports:
            # ("Gs3", "minor") - simple
            # ("Gs3", "minor", 1) - with inversion
            # ("Gs3", "minor", {"inversion": 1, "openness": 0.3}) - with kwargs dict
            # ("Gs3", "minor", 1, {"openness": 0.3}) - mixed: positional args + kwargs
            
            if isinstance(chord_item[-1], dict):
                # Last element is dict - extract it for kwargs
                kwargs = chord_item[-1]
                args = chord_item[:-1]
            else:
                # No dict at end, all positional args
                kwargs = {}
                args = chord_item
            
            # Use build_chord library function with unpacked args and kwargs
            chord_notes = build_chord(*args, **kwargs)
            
            # Apply smooth voicing if enabled and not first chord
            if smooth_voicing and previous_chord_notes is not None:
                chord_notes = find_chord_voicing_by_common_tones(previous_chord_notes, chord_notes)
            
            chord_duration = chord_durations[chord_idx]
            
            # Get pattern for this chord
            if patterns is None:
                # No pattern: play all chord notes once for full duration
                pattern = [1]
            else:
                # Get the pattern (either single pattern or per-chord)
                if isinstance(patterns[0], (list, tuple)):
                    # Per-chord patterns
                    pattern = patterns[chord_idx] if chord_idx < len(patterns) else patterns[0]
                else:
                    # Single pattern for all chords
                    pattern = patterns
            
            # Play chord multiple times according to pattern
            pattern_sum = sum(pattern)
            pattern_time = current_time
            
            for pattern_idx, pattern_value in enumerate(pattern):
                # Duration for this chord playback
                note_duration = (chord_duration * pattern_value) / pattern_sum
                
                # Play ALL notes of the chord together
                for midi_note in chord_notes:
                    midi.addNote(0, 0, midi_note, pattern_time, note_duration, volume)
                
                pattern_time += note_duration
            
            current_time += chord_duration
            previous_chord_notes = chord_notes  # Save for next iteration
    
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
