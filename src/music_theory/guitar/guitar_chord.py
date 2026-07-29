from src.music_theory.core.notes import note_string_to_midi

STANDARD_GUITAR_TUNING_NOTES = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
STANDARD_GUITAR_TUNING_MIDI = [note_string_to_midi(x) for x in STANDARD_GUITAR_TUNING_NOTES]


def get_chord_from_tabs(tabs):
    """
    Get MIDI notes for a chord from guitar tablature positions.

    Args:
        tabs: List of fret positions for each string (-1 = not played)

    Returns:
        List of MIDI note numbers
    """
    chord = STANDARD_GUITAR_TUNING_MIDI[::]
    for i, fret_position in enumerate(tabs):
        if fret_position != -1:
            chord[i] += fret_position
    return chord
