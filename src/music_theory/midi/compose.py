"""
Chord composition utilities for generating MIDI progressions.

Converts chord-token specifications into full MIDI chord progressions.
"""

from pathlib import Path
from midiutil import MIDIFile
from src.music_theory.core.notes import build_chord, find_chord_voicing_by_common_tones
from src.music_theory.core.chord import ChordEvent


def compose_chord_progression(sections, output_file=None, tempo=120, volume=70,
                              smooth_voicing=False, verbose=False):
    """
    Generate a chord progression from note/chord type pairs, supporting multiple sections.
    
    Args:
        sections: List of (chords, chord_durations, patterns, loop_count) tuples.
                 Each section represents a separate progression segment with its own configuration.
        output_file: Path to save MIDI file. If None, returns MIDIFile object.
        tempo: Tempo in BPM (default 120)
        volume: MIDI volume 0-127 (default 70)
        smooth_voicing: If True, uses find_chord_voicing_by_common_tones() to smooth voice
                       leading between consecutive chords, minimizing note movement (default False).
                       Note: smooth voicing persists across section boundaries.
        verbose: Print debug info (default False)
    
    Returns:
        None if output_file is specified, otherwise MIDIFile object
    """
    midi = MIDIFile(1)
    midi.addTempo(0, 0, tempo)

    current_time = 0
    
    # Initialize previous_chord_notes to the last chord of the progression
    # This allows the first chord to smooth-lead from the end, creating a loop
    if smooth_voicing and sections:
        last_section = sections[-1]
        last_chords = last_section[0]  # Get chords list from last section
        if last_chords:
            last_chord_item = last_chords[-1]
            previous_chord_notes = _build_chord_event(last_chord_item)
        else:
            previous_chord_notes = None
    else:
        previous_chord_notes = None

    for section_idx, section in enumerate(sections):
        chords, chord_durations, patterns, loop_count = section
        
        # Default durations
        if chord_durations is None:
            chord_durations = [4] * len(chords)

        # Loop the entire chord progression
        for loop_idx in range(loop_count):
            for chord_idx, chord_item in enumerate(chords):
                chord_notes = _build_chord_event(chord_item)

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


def _build_chord_event(chord_item):
    """Build a chord from a token or a :class:`ChordEvent`."""
    if isinstance(chord_item, ChordEvent):
        return build_chord(chord_item.chord, **chord_item.build_kwargs())
    if isinstance(chord_item, str):
        return build_chord(chord_item)
    raise TypeError(
        "Chord entries must be chord-token strings or ChordEvent instances."
    )
