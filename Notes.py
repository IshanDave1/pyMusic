from typing import List, Union

from Constants import notes, scales, chords, interval_half_steps


def get_num(note: str) -> int:
    if not (note[-1].isdigit() and note[:-1] in notes):
        raise ValueError(
            f"note {note[-1]} The note can only be A-G , only C,D,F,G,A can be flat and the octave has to be a number")
    return notes.index(note[:-1]) + int(note[-1]) * 12

def get_chord_from_notes(notes_list: Union[List[int],List[str]]):
    if type(notes_list) == list:
        if type(notes_list[0]) == str:
            notes_list = [get_num(x) for x in notes_list]
    notes_list.sort()
    print(notes_list)
    for base_note in [x-12 for x in notes_list]+notes_list:
        for chord_type,intervals in chords.items():
            for inversion in range(len(intervals)):
                if get_chord(base_note, chord_type, inversion=inversion) == notes_list:
                    if inversion == 0 :
                        inversion_part = ""
                    elif inversion == 1 :
                        inversion_part = "1st  inversion"
                    elif inversion == 2 :
                        inversion_part = "2nd  inversion"
                    elif inversion == 3 :
                        inversion_part = "3rd  inversion"
                    else :
                        inversion_part = f"{inversion}th"
                    print(f"{get_note(base_note)} {chord_type} {inversion_part}")
            # print(get_chord(base_note, chord_type, inversion=inversion) )


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
