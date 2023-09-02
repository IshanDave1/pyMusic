from typing import List, Tuple, Union

notes = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]
scales = {
    'major': [2, 2, 1, 2, 2, 2, 1],
    'minor': [2, 1, 2, 2, 1, 2, 2],
    'harmonic_minor': [2, 1, 2, 2, 1, 3, 1],
    'dorian': [2, 1, 2, 2, 2, 1, 2],
    'phrygian': [1, 2, 2, 2, 1, 2, 2],
    'lydian': [2, 2, 2, 1, 2, 2, 1],
    'mixolydian': [2, 2, 1, 2, 2, 1, 2],
    'aeolian': [2, 1, 2, 2, 1, 2, 2],  # same as minor
    'locrian': [1, 2, 2, 1, 2, 2, 2],
}

interval_half_steps = {
    "unison": 0,
    "minor_second": 1,
    "major_second": 2,
    "minor_third": 3,
    "major_third": 4,
    "perfect_fourth": 5,
    "tritone": 6,
    "perfect_fifth": 7,
    "minor_sixth": 8,
    "major_sixth": 9,
    "minor_seventh": 10,
    "major_seventh": 11,
    "octave": 12,
}

chords = {
    'major': ['unison', 'major_third', 'perfect_fifth'],
    'minor': ['unison', 'minor_third', 'perfect_fifth'],
    'diminished': ['unison', 'minor_third', 'tritone'],
    'augmented': ['unison', 'major_third', 'minor_sixth'],
    'sus2': ['unison', 'major_second', 'perfect_fifth'],
    'sus4': ['unison', 'perfect_fourth', 'perfect_fifth'],
    'major_seventh': ['unison', 'major_third', 'perfect_fifth', 'major_seventh'],
    'minor_seventh': ['unison', 'minor_third', 'perfect_fifth', 'minor_seventh'],
    'dominant_seventh': ['unison', 'major_third', 'perfect_fifth', 'minor_seventh'],
    'diminished_seventh': ['unison', 'minor_third', 'tritone', 'major_sixth'],
    'half_diminished_seventh': ['unison', 'minor_third', 'tritone', 'minor_seventh'],
    'augmented_major_seventh': ['unison', 'major_third', 'minor_sixth', 'major_seventh'],
    'augmented_minor_seventh': ['unison', 'major_third', 'minor_sixth', 'minor_seventh'],
}


def get_num(note: str) -> int:
    return notes.index(note[:len(note)-1]) + int(note[-1]) * 12


def get_note(num: int) -> str:
    return f"{notes[num % 12]}{num // 12}"


def get_scale_num(num: Union[int, str], scale_type: str) -> List[int]:
    if type(num) == str:
        num = get_num(num)
    return [num + sum(scales[scale_type][:i]) for i in range(7)]


def get_scale_notes(num: Union[int, str], scale_type: str) -> List[str]:
    return [get_note(n) for n in get_scale_num(num, scale_type)]


def get_chord(base_note, chord_type, inversion=1):
    pass


