import math
from typing import List, Union, Set, Dict

import numpy

from MusicTheory.constants import *


def get_num(note: str) -> int:
    if any(n.lower() == note.lower() for n in notes):
        return [n.lower() == note.lower() for n in notes].index(True) + middle_octave * 12
    elif note[-1].isdigit() and any(n.lower() == note[:-1].lower() for n in notes):
        return [n.lower() == note[:-1].lower() for n in notes].index(True) + int(note[-1]) * 12
    else:
        raise ValueError(
            f"note {note[-1]} The note can only be A-G , B and E can't be sharp the octave has to be a number")


def get_note(num: int) -> str:
    if num < min_note or num > max_note:
        raise ValueError(f"num {num} has to be in range 0-100")
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


def get_scale_degree(note: Union[int, str], scale_type: str, degree: int) -> int:
    return get_scale_num(note, scale_type)[degree - 1]


def get_scale_chord(note: Union[int, str], scale_type: str, degree: int, num_notes: int) -> List[int]:
    scale = get_scale_num(note, scale_type) + get_scale_num(get_transpose_num(note), scale_type) + get_scale_num(
        get_transpose_num(note, 24), scale_type)
    c_notes = [degree - 1 + 2 * i for i in range(num_notes)]
    return [scale[c_note] for c_note in c_notes]


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

    all_inversions = list(filter(lambda x: is_same_inversion(x, base_part), get_inversion(base_part, over_octaves)))
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


def get_inversion_unfiltered(chord: List[int], octaves: int) -> List[List[int]]:
    chord_in_octaves = [[note + 12 * octave for octave in range(octaves)] for note in chord]

    def helper(lol):
        if len(lol) == 1:
            return [[x] for x in lol[0]]
        lol_sub = helper(lol[:-1])
        return [l + [ele] for l in lol_sub for ele in lol[-1]]

    inv = helper(chord_in_octaves)

    def get_evenness(lis):
        return numpy.prod([lis[i] - lis[i - 1] for i in range(1, len(lis))])

    return list(sorted([sorted(ch) for ch in inv], key=lambda x: get_evenness(x)))


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
    chord_two_possibilities = get_inversion_unfiltered(get_chord(get_transpose_num(base_note2, -12), chord_type2), 3)
    chord_one = get_chord(base_note, chord_type, inversion)
    return min(chord_two_possibilities, key=lambda chord_two: get_taxicab_chord_distance_chord(chord_one, chord_two))


def get_closest_taxicab_inversion_chord(chord_one: List[int], chord_2: List[int]) -> List[int]:
    chord_two_possibilities = get_inversion_unfiltered([get_transpose_num(note, -12) for note in chord_2], 3)
    return min(chord_two_possibilities, key=lambda chord_two: get_taxicab_chord_distance_chord(chord_one, chord_two))
