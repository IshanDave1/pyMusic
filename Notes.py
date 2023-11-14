import math
from typing import List, Union, Set, Dict

import numpy

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
            f"note {note[-1]} The note can only be A-G , only C,D,F,G,A can be sharp and the octave has to be a number")
    return notes.index(note[:-1]) + int(note[-1]) * 12


def get_note(num: int) -> str:
    if num <= 0 or num >= 100:
        raise ValueError(
            f"num {num} has to be in range 0-100"
        )
    return f"{notes[num % 12]}{num // 12}"


def get_transpose_note(note: Union[int, str], semitones: int = 12) -> str:
    if type(note) == str:
        note = get_num(note)
    return get_note(note + semitones)


def get_transpose_num(note: Union[int, str], semitones: int = 12) -> int:
    if type(note) == str:
        note = get_num(note)
    return note + semitones


def get_scale_num(num: Union[int, str], scale_type: str) -> List[int]:
    if scale_type not in scales.keys():
        raise ValueError(f"not supported scale {scale_type}")
    if type(num) == str:
        num = get_num(num)
    return [num + sum(scales[scale_type][:i]) for i in range(len(scales[scale_type]))]


def get_scale_notes(num: Union[int, str], scale_type: str) -> List[str]:
    return [get_note(n) for n in get_scale_num(num, scale_type)]


def get_chord(base_note: Union[int, str], chord_type: str, inversion: int = 0, lo_double_notes: List[int] = None,
              uo_double_notes: List[int] = None, over_octaves=1,
              openness: float = 0.0, rootless=False) -> List[int]:
    if interval_half_steps[chords[chord_type][-1]] > 12:
        over_octaves = max(over_octaves, 2)
    if openness < 0 or openness >= 1:
        raise ValueError(f"openness is {openness} it has to be in range [0,1)")
    if chord_type not in chords.keys():
        raise ValueError(f"not supported chord {chord_type}")
    if type(base_note) == str:
        base_note = get_num(base_note)

    if lo_double_notes is None:
        lo_double_notes = []
    if uo_double_notes is None:
        uo_double_notes = []
    root_position = [base_note + interval_half_steps[ele] for ele in chords[chord_type]]
    lo_notes = [get_transpose_num(root_position[index], -12) for index in lo_double_notes]
    uo_notes = [get_transpose_num(root_position[index]) for index in uo_double_notes]
    base_part = root_position[inversion:]
    transposed_part = [get_transpose_num(note) for note in root_position][:inversion]
    base_part.extend(transposed_part)
    base_part.sort()

    # print(base_part)
    all_inversions = list(filter(lambda x: is_same_inversion(x, base_part), get_inversion(base_part, over_octaves)))
    # print(len(get_inversion(base_part, over_octaves)))
    # print(all_inversions)
    # print(math.floor(openness * len(all_inversions)))
    base_part = all_inversions[math.floor(openness * len(all_inversions))]
    base_part.extend(lo_notes)
    base_part.extend(uo_notes)

    return sorted(base_part)


def get_inversion(chord: List[int], octaves: int) -> List[List[int]]:
    chord_in_octaves = [[note + 12 * octave for octave in range(octaves)] for note in chord]

    def helper(lol):
        if len(lol) == 1:
            return [[x] for x in lol[0]]
        lol_sub = helper(lol[:-1])
        return [l + [ele] for l in lol_sub for ele in lol[-1]]

    inv = helper(chord_in_octaves)

    def get_evenness(lis):
        return numpy.prod([lis[i] - lis[i - 1] for i in range(1, len(lis))])

    return list(filter(lambda x: x[-1] - x[0] >= 12 * (octaves - 1),
                       sorted([sorted(ch) for ch in inv], key=lambda x: get_evenness(x))))


def is_same_chord(c1: List[int], c2: List[int]) -> bool:
    return {x % 12 for x in c1} == {x % 12 for x in c2}


def is_same_inversion(c1: List[int], c2: List[int]) -> bool:
    return all(x1 % 12 == x2 % 12 for x1, x2 in zip(c1, c2))


def get_chord_from_notes(notes_as_list: Set[int]) -> Dict[str, List[int]]:
    def is_in_Set(ch, nts) -> bool:
        return all(x in nts for x in ch)

    all_chords = {}
    for note in notes_as_list:
        for chord in chords:
            chord_as_list = get_chord(note, chord)
            if is_in_Set({x % 12 for x in chord_as_list}, {x % 12 for x in notes_as_list}):
                all_chords[f"{get_note(note)} {chord}"] = chord_as_list

    return all_chords


scl = [get_num(x) for x in ["C4", 'Cs4', 'F4', 'Gs4', 'Ds4', 'As4', 'G4']]
l = get_chord_from_notes(scl)
filtered_dict = {k: [get_note(x) for x in v] for k, v in l.items() if len(v) in {4}}
print(filtered_dict)


def get_mean_chord_distance(base_note: Union[int, str], chord_type, base_note2: Union[int, str], chord_type2,
                            inversion=0, inversion2=0) -> float:
    return get_mean_chord_distance_chord(get_chord(base_note, chord_type, inversion),
                                         get_chord(base_note2, chord_type2, inversion2))


def get_mean_chord_distance_chord(chord1: List[int], chord2: List[int]) -> float:
    return abs(sum(chord1) / len(chord1) - sum(chord2) / len(chord2))


def get_taxicab_chord_distance_chord(chord1: List[int], chord2: List[int]) -> float:
    if len(chord1) > len(chord2):
        get_taxicab_chord_distance_chord(chord2, chord1)
    c1 = sorted(chord1)
    c2 = sorted(chord2)
    delta_l = len(c2) - len(c1)
    dist = 10000
    for i in range(delta_l + 1):
        dist = min(dist, sum(abs(c2[i + j] - c1[j]) for j in range(len(c1))))
    return dist


def get_taxicab_chord_distance(base_note: Union[int, str], chord_type, base_note2: Union[int, str], chord_type2,
                               inversion=0, inversion2=0) -> float:
    return get_taxicab_chord_distance_chord(get_chord(base_note, chord_type, inversion),
                                            get_chord(base_note2, chord_type2, inversion2))


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


def get_closest_taxicab_inversion(base_note: Union[int, str], chord_type, base_note2: Union[int, str], chord_type2,
                                  inversion) -> List[int]:
    chord_two_possibilities = get_inversion(get_chord(get_transpose_num(base_note2, -12), chord_type2), 3)
    chord_one = get_chord(base_note, chord_type, inversion)
    print(chord_two_possibilities)
    return min(chord_two_possibilities, key=lambda chord_two: get_taxicab_chord_distance_chord(chord_one, chord_two))


print([get_note(x) for x in get_chord('D4', 'minor_seventh', 0)])
print([get_note(x) for x in get_chord('C4', 'major_seventh', 0)])
print(is_same_chord([48, 52, 55, 59], [48, 52, 55, 59]))
print([get_note(x) for x in get_closest_taxicab_inversion('D4', 'minor_seventh', 'C4', 'major_seventh', 0)])
