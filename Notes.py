from typing import List, Union

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
    'minor_pentatonic': [3, 2, 2, 3, 2],
    'major_pentatonic': [2, 2, 3, 2, 3],
    'major_blues': [2, 1, 1, 3, 2, 3],
    'minor_blues': [3, 2, 1, 1, 3, 2]

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
    "minor_ninth": 13,
    "major_ninth": 14,
    "minor_eleventh": 16,
    "major_eleventh": 17,
    "minor_thirteenth": 22,
    "major_thirteenth": 23,
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
    'minor_major_seventh': ['unison', 'minor_third', 'perfect_fifth', 'major_seventh'],
    'dominant_seventh': ['unison', 'major_third', 'perfect_fifth', 'minor_seventh'],
    'diminished_seventh': ['unison', 'minor_third', 'tritone', 'major_sixth'],
    'half_diminished_seventh': ['unison', 'minor_third', 'tritone', 'minor_seventh'],
    'augmented_major_seventh': ['unison', 'major_third', 'minor_sixth', 'major_seventh'],
    'augmented_minor_seventh': ['unison', 'major_third', 'minor_sixth', 'minor_seventh'],
    'major_seventh_flat_five': ['unison', 'major_third', 'tritone', 'major_seventh'],
    'minor_seventh_flat_five': ['unison', 'minor_third', 'tritone', 'minor_seventh'],
    'major_seventh_sharp_five': ['unison', 'major_third', 'minor_sixth', 'major_seventh'],
    'minor_seventh_sharp_five': ['unison', 'minor_third', 'minor_sixth', 'major_seventh'],
    'dominant_ninth': ['unison', 'major_third', 'perfect_fifth', 'minor_seventh', 'major_ninth'],
    'major_ninth': ['unison', 'major_third', 'perfect_fifth', 'major_seventh', 'major_ninth'],
    'minor_ninth': ['unison', 'minor_third', 'perfect_fifth', 'minor_seventh', 'major_ninth'],
    'dominant_thirteenth': ['unison', 'major_third', 'perfect_fifth', 'minor_seventh', 'major_ninth',
                            'major_thirteenth'],
    'major_thirteenth': ['unison', 'major_third', 'perfect_fifth', 'major_seventh', 'major_ninth', 'major_thirteenth'],
    # The major eleventh is often omitted because it clashes with the major third
    'minor_thirteenth': ['unison', 'minor_third', 'perfect_fifth', 'minor_seventh', 'major_ninth', 'major_thirteenth'],
    # The major eleventh is often omitted because it clashes with the major third
    'minor_eleventh': ['unison', 'minor_third', 'perfect_fifth', 'minor_seventh', 'minor_eleventh'],
    'major_eleventh': ['unison', 'major_third', 'perfect_fifth', 'major_seventh', 'major_eleventh'],
    'sus9': ['unison', 'major_second', 'perfect_fifth', 'major_ninth'],
    'add9': ['unison', 'major_second', 'major_third', 'perfect_fifth', 'major_ninth'],
    '6/9': ['unison', 'major_second', 'major_third', 'perfect_fifth', 'major_sixth', 'major_ninth'],
    'minor_sixth': ['unison', 'minor_third', 'perfect_fifth', 'major_sixth'],
    'major_sixth': ['unison', 'major_third', 'perfect_fifth', 'major_sixth']
}


def get_num(note: str) -> int:
    if not (note[-1].isdigit() and note[:-1] in notes):
        raise ValueError(
            f"note {note[-1]} The note can only be A-G , only C,D,F,G,A can be flat and the octave has to be a number")
    return notes.index(note[:-1]) + int(note[-1]) * 12


def get_note(num: int) -> str:
    return f"{notes[num % 12]}{num // 12}"


def get_transpose_note(note: Union[int, str], semitones: int = 12) -> str:
    if type(note) == str:
        note = get_num(note)
    return get_note(note + semitones)


def get_transpose_num(note: Union[int, str], octave: int = 1) -> int:
    if type(note) == str:
        note = get_num(note)
    return note + 12 * octave


def get_scale_num(num: Union[int, str], scale_type: str) -> List[int]:
    if scale_type not in scales.keys():
        raise ValueError(f"not supported scale {scale_type}")
    if type(num) == str:
        num = get_num(num)
    return [num + sum(scales[scale_type][:i]) for i in range(len(scales[scale_type]))]


def get_scale_notes(num: Union[int, str], scale_type: str) -> List[str]:
    return [get_note(n) for n in get_scale_num(num, scale_type)]


def get_chord(base_note: Union[int, str], chord_type, inversion=0, open=True):
    if chord_type not in chords.keys():
        raise ValueError(f"not supported chord {chord_type}")
    if inversion > 0:
        base_part = get_chord(base_note, chord_type)[inversion:]
        transposed_part = get_chord(get_transpose_num(base_note), chord_type)[:inversion]
        base_part.extend(transposed_part)
        return base_part

    if type(base_note) == str:
        base_note = get_num(base_note)
    return [base_note + interval_half_steps[ele] for ele in chords[chord_type]]


def get_mean_chord_distance(base_note: Union[int, str], chord_type, base_note2: Union[int, str], chord_type2,
                            inversion=0, inversion2=0) -> float:
    return get_mean_chord_distance_chord(get_chord(base_note, chord_type, inversion),
                                         get_chord(base_note2, chord_type2, inversion2))


def get_mean_chord_distance_chord(chord1: List[int], chord2: List[int]) -> float:
    return abs(sum(chord1) / len(chord1) - sum(chord2) / len(chord2))


def get_closest_inversion(base_note: Union[int, str], chord_type, base_note2: Union[int, str], chord_type2,
                          inversion) -> List[int]:
    return min(
        (
            (get_mean_chord_distance(
                base_note, chord_type, base_note2, chord_type2, inversion, inv
            ), get_chord(base_note2, chord_type2, inv))
            for inv in range(len(chords[chord_type2]))
        ),
        key=lambda x: x[0],
    )[1]
