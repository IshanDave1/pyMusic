import random
from pathlib import Path
from midiutil import MIDIFile

raag = {
    "aaroh": [1,2,4,5,"6b","7b"],
    "avroh": [1,2,"3b",4,5,"6b","7b"],
    "rules" : {
        "nivas_notes" : [1,"3b","6b","7b"],
    }
}

def generate_melody(raag, length):
    current_note_index = 0
    melody = [(get_note_at_index(raag, current_note_index, "aaroh"), 1)]
    for i in range(length):
        next_note_index, duration_next_note = generate_next_note(raag, current_note_index)
        if next_note_index > current_note_index:
            melody.append((get_note_at_index(raag, next_note_index, "aaroh", 60), duration_next_note))
        else:
            melody.append((get_note_at_index(raag, next_note_index, "avroh", 60), duration_next_note))

        current_note_index = next_note_index
    return melody


def generate_next_note(raag, current_note_index) -> int:
    """
    Generate the next note index in a raag melody.
    
    Returns:
        Tuple of (next_note_index, duration_for_next_note)
    """
    probability_right = 0.5
    probability_jump = 0.1
    max_right_index = 10
    max_left_index = -6
    if current_note_index < max_left_index:
        probability_right = 1
    if current_note_index > max_right_index:
        probability_right = 0
    will_move_right = random.uniform(0, 1) < probability_right
    will_jump = random.uniform(0, 1) < probability_jump
    if will_move_right:
        if will_jump:
            next_note_index = current_note_index + 2
        else:
            next_note_index = current_note_index + 1
    else:
        if will_jump:
            next_note_index = current_note_index - 2
        else:
            next_note_index = current_note_index - 1
    duration = random.choices([0.25, 0.5, 1], weights=[1, 2, 1])[0]
    for note_rule in raag["rules"]["nivas_notes"]:
        if parse_solfege(note_rule) == get_note_at_index(raag, next_note_index, "aaroh" if will_move_right else "avroh") % 12:
            duration = 1
    return next_note_index, duration


def get_note_at_index(raag, index, scale_direction, base_note=60):
    """
    Get MIDI note at the given index in the raag scale.

    Args:
        raag: Dictionary with "aaroh" containing solfège notation
        index: Index in the scale (supports negatives and ±2 octaves)
        scale_direction: Direction ("aaroh" for ascending, "avroh" for descending)
        base_note: MIDI note for Sa (default 60 = C4)

    Returns:
        MIDI note number
    """
    scale = raag[scale_direction]
    scale_length = len(scale)

    # Normalize index to get position within scale and octave offset
    octave_offset = index // scale_length
    position = index % scale_length

    # Get the note spec at this position and parse it
    note_spec = scale[position]
    semitone_offset = parse_solfege(note_spec)

    # Calculate final MIDI note
    midi_note = base_note + semitone_offset + (octave_offset * 12)

    return midi_note


def parse_solfege(note_spec):
    """Convert solfège notation to semitone offset from Sa."""
    # Default shuddha (natural) intervals in semitones from Sa
    solfege_intervals = {
        '1': 0,   # Sa
        '2': 2,   # Re (shuddha)
        '3': 4,   # Ga (shuddha)
        '4': 5,   # Ma
        '5': 7,   # Pa
        '6': 9,   # Dha (shuddha)
        '7': 11,  # Ni
    }

    # Handle string or int input
    note_spec = str(note_spec)

    # Extract base degree and accidentals
    degree = note_spec[0]
    accidentals = note_spec[1:]

    interval = solfege_intervals.get(degree, 0)

    # Apply accidentals: 's' = sharp (+1), 'b' = flat (-1)
    for char in accidentals:
        if char == 's':
            interval += 1
        elif char == 'b':
            interval -= 1

    return interval


def melody_to_midi(melody, output_file=None, tempo=180, volume=48, beat_duration=4, return_midi=False):
    """
    Convert a melody to a MIDI file or MIDIFile object.

    Args:
        melody: List of tuples (midi_note, duration) where duration is in whole notes
        output_file: Path to write the MIDI file (if None and return_midi=True, returns MIDIFile object)
        tempo: Tempo in BPM (default 180)
        volume: MIDI volume 0-127 (default 48)
        beat_duration: Beats per whole note (default 4, standard in 4/4 time)
        return_midi: If True and output_file is None, return MIDIFile object instead of writing

    Returns:
        MIDIFile object if return_midi=True and output_file=None, otherwise None
    """
    track = 0
    channel = 0
    time = 0

    midi = MIDIFile(1)
    midi.addTempo(track, 0, tempo)

    current_time = 0
    for note_midi, duration in melody:
        # Convert whole note duration to beats
        duration_in_beats = duration * beat_duration
        will_pause = random.uniform(0, 1) < 0.8
        midi.addNote(track, channel, note_midi, current_time, duration_in_beats, volume)
        current_time += duration_in_beats

    if output_file is not None:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "wb") as f:
            midi.writeFile(f)
        return None
    elif return_midi:
        return midi
    else:
        return None


def generate_raga_melody_prog(length=256, output_file=None, tempo=240, volume=80, 
                               beat_duration=4, verbose=False):
    """
    Convenience wrapper for generating complete raga melodies.
    
    Generates an Indian classical (raga) melody and optionally saves to MIDI file.
    
    Args:
        length: Length of melody in note indices (default 256)
        output_file: Path to save MIDI file. If None, returns MIDIFile object.
        tempo: Tempo in BPM (default 240)
        volume: MIDI volume 0-127 (default 80)
        beat_duration: Beats per whole note (default 4)
        verbose: Print debug info (default False)
    
    Returns:
        None if output_file is specified, otherwise MIDIFile object
    """
    melody = generate_melody(raag, length)
    
    midi = melody_to_midi(
        melody,
        output_file=output_file,
        tempo=tempo,
        volume=volume,
        beat_duration=beat_duration,
        return_midi=(output_file is None)
    )
    
    if verbose and output_file:
        print(f"  Wrote: {output_file}")
    
    return midi