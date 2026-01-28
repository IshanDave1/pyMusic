"""
Notes module for music theory operations.

This module provides comprehensive utilities for working with musical notes,
scales, chords, and voice leading. It supports MIDI note numbers and string
representations (e.g., "C5", "Fs4") and includes functions for transposition,
scale generation, chord construction with advanced voicing options, and
finding optimal chord inversions for smooth voice leading.

Note naming convention:
    - Notes are named A-G with 's' suffix for sharps (e.g., Cs, Fs, Gs)
    - Octave numbers follow the note name (e.g., C5 = middle C + 1 octave)
    - MIDI note 60 = C5 (middle C in this system)
"""

import math
from typing import List, Union, Set, Dict

import numpy

from MusicTheory.constants import *


def get_num(note: str) -> int:
    """
    Convert a note string to its MIDI note number.

    Args:
        note: A note string in format "NoteName" or "NoteNameOctave".
              Examples: "C", "C5", "Fs4", "Gs"
              If no octave is specified, uses middle_octave from constants.

    Returns:
        The MIDI note number (0-127 range typically).

    Raises:
        ValueError: If the note string is invalid.

    Examples:
        >>> get_num("C5")
        60
        >>> get_num("Fs4")
        54
        >>> get_num("C")  # Uses middle_octave default
        60
    """
    if any(n.lower() == note.lower() for n in notes):
        return [n.lower() == note.lower() for n in notes].index(True) + middle_octave * 12
    elif note[-1].isdigit() and any(n.lower() == note[:-1].lower() for n in notes):
        return [n.lower() == note[:-1].lower() for n in notes].index(True) + int(note[-1]) * 12
    else:
        raise ValueError(
            f"Invalid note '{note}'. Notes must be A-G (with optional sharp 's' suffix: Cs, Ds, Fs, Gs, As) followed by an octave number.")


def get_note(num: int) -> str:
    """
    Convert a MIDI note number to its string representation.

    Args:
        num: MIDI note number (must be within min_note to max_note range).

    Returns:
        Note string in format "NoteNameOctave" (e.g., "C5", "Fs4").

    Raises:
        ValueError: If num is outside the valid range.

    Examples:
        >>> get_note(60)
        'C5'
        >>> get_note(66)
        'Fs5'
    """
    if num < min_note or num > max_note:
        raise ValueError(f"num {num} has to be in range 0-100")
    return f"{notes[num % 12]}{num // 12}"


def get_transpose_note(note: Union[int, str], semitones: int = 12) -> str:
    """
    Transpose a note by a number of semitones and return as string.

    Args:
        note: The note to transpose (MIDI number or string like "C5").
        semitones: Number of semitones to transpose. Default is 12 (one octave up).
                   Negative values transpose down.

    Returns:
        The transposed note as a string.

    Examples:
        >>> get_transpose_note("C5")
        'C6'
        >>> get_transpose_note("C5", -12)
        'C4'
        >>> get_transpose_note(60, 7)
        'G5'
    """
    if type(note) == str:
        note = get_num(note)
    return get_note(note + semitones)


def get_transpose_num(note: Union[int, str], semitones: int = 12) -> int:
    """
    Transpose a note by a number of semitones and return as MIDI number.

    Args:
        note: The note to transpose (MIDI number or string like "C5").
        semitones: Number of semitones to transpose. Default is 12 (one octave up).
                   Negative values transpose down.

    Returns:
        The transposed note as a MIDI number.

    Examples:
        >>> get_transpose_num("C5")
        72
        >>> get_transpose_num(60, -12)
        48
    """
    if type(note) == str:
        note = get_num(note)
    return note + semitones


def get_scale_num(num: Union[int, str], scale_type: str) -> List[int]:
    """
    Generate a scale as a list of MIDI note numbers.

    Args:
        num: The root note of the scale (MIDI number or string).
        scale_type: The type of scale (e.g., "major", "minor", "dorian").
                    Must be a key in the scales dictionary from constants.

    Returns:
        A list of MIDI note numbers representing the scale.

    Raises:
        ValueError: If scale_type is not supported.

    Examples:
        >>> get_scale_num(60, "major")
        [60, 62, 64, 65, 67, 69, 71]
        >>> get_scale_num("C5", "minor")
        [60, 62, 63, 65, 67, 68, 70]
    """
    if scale_type not in scales.keys():
        raise ValueError(f"not supported scale {scale_type}")
    if type(num) == str:
        num = get_num(num)
    return [num + sum(scales[scale_type][:i]) for i in range(len(scales[scale_type]))]


def get_scale_degree(note: Union[int, str], scale_type: str, degree: int) -> int:
    """
    Get a specific scale degree as a MIDI note number.

    Args:
        note: The root note of the scale (MIDI number or string).
        scale_type: The type of scale (e.g., "major", "minor").
        degree: The scale degree (1-based). 1 = root, 2 = second, etc.

    Returns:
        The MIDI note number of the requested scale degree.

    Examples:
        >>> get_scale_degree("C5", "major", 5)  # The 5th degree (G)
        67
        >>> get_scale_degree(60, "major", 3)  # The 3rd degree (E)
        64
    """
    return get_scale_num(note, scale_type)[degree - 1]


def get_scale_chord(note: Union[int, str], scale_type: str, degree: int, num_notes: int) -> List[int]:
    """
    Build a chord from scale degrees (diatonic chord).

    Constructs a chord by stacking thirds from the specified scale degree.
    This creates diatonic chords that naturally fit within the scale.

    Args:
        note: The root note of the scale (MIDI number or string).
        scale_type: The type of scale (e.g., "major", "minor").
        degree: The scale degree to build the chord on (1-based).
        num_notes: Number of notes in the chord (3 = triad, 4 = 7th, etc.).

    Returns:
        A list of MIDI note numbers representing the chord.

    Examples:
        >>> get_scale_chord("C5", "major", 1, 3)  # C major triad
        [60, 64, 67]
        >>> get_scale_chord("C5", "major", 2, 4)  # Dm7
        [62, 65, 69, 72]
    """
    scale = get_scale_num(note, scale_type) + get_scale_num(get_transpose_num(note), scale_type) + get_scale_num(
        get_transpose_num(note, 24), scale_type)
    c_notes = [degree - 1 + 2 * i for i in range(num_notes)]
    return [scale[c_note] for c_note in c_notes]


def get_scale_notes(num: Union[int, str], scale_type: str) -> List[str]:
    """
    Generate a scale as a list of note name strings.

    Args:
        num: The root note of the scale (MIDI number or string).
        scale_type: The type of scale (e.g., "major", "minor", "dorian").

    Returns:
        A list of note strings representing the scale.

    Examples:
        >>> get_scale_notes(60, "major")
        ['C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5']
    """
    return [get_note(n) for n in get_scale_num(num, scale_type)]


def get_chord(base_note: Union[int, str], chord_type: str, inversion: int = 0, lo_double_notes: List[int] = None,
              uo_double_notes: List[int] = None, over_octaves=1,
              openness: float = 0.0, rootless=False) -> List[int]:
    """
    Generate a chord with advanced voicing options.

    Creates a chord based on the chord type with support for inversions,
    octave doubling, spread voicings, and openness control.

    Args:
        base_note: The root note of the chord (MIDI number or string).
        chord_type: The type of chord (e.g., "major", "minor", "dominant_seventh").
                    Must be a key in the chords dictionary from constants.
        inversion: The inversion number (0 = root position, 1 = first inversion, etc.).
        lo_double_notes: List of chord tone indices to double in the lower octave.
        uo_double_notes: List of chord tone indices to double in the upper octave.
        over_octaves: Number of octaves to spread the chord over. Automatically
                      increased to 2 for extended chords (9ths, 11ths, 13ths).
        openness: A float in range [0, 1) controlling voicing spread.
                  0 = closest voicing, approaching 1 = more open/spread voicing.
        rootless: Reserved for future use (rootless voicings).

    Returns:
        A sorted list of MIDI note numbers representing the chord.

    Raises:
        ValueError: If chord_type is not supported or openness is out of range.

    Examples:
        >>> get_chord("C5", "major")
        [60, 64, 67]
        >>> get_chord(60, "major", inversion=1)  # First inversion
        [64, 67, 72]
        >>> get_chord("C5", "major_seventh", openness=0.5)  # More spread voicing
        [60, 67, 71, 76]
    """
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
    """
    Generate all possible voicings of a chord across multiple octaves.

    Creates all combinations of chord tones spread across the specified
    number of octaves, filtered to ensure proper voice spacing and sorted
    by evenness of voice distribution.

    Args:
        chord: A list of MIDI note numbers representing the chord.
        octaves: Number of octaves to spread voicings across.

    Returns:
        A list of chord voicings (each a list of MIDI notes), filtered to
        ensure the voicing spans at least (octaves-1) * 12 semitones,
        sorted by evenness of note spacing.

    Example:
        >>> chord = [60, 64, 67]  # C major
        >>> voicings = get_inversion(chord, 2)
        >>> # Returns various spread voicings of C major across 2 octaves
    """
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
    """
    Generate all possible voicings of a chord without span filtering.

    Similar to get_inversion but without the minimum span requirement,
    returning all possible combinations sorted by evenness.

    Args:
        chord: A list of MIDI note numbers representing the chord.
        octaves: Number of octaves to spread voicings across.

    Returns:
        A list of all chord voicings sorted by evenness of note spacing.
        Unlike get_inversion, includes tightly-spaced voicings.

    Example:
        >>> chord = [60, 64, 67]
        >>> all_voicings = get_inversion_unfiltered(chord, 2)
    """
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
    """
    Check if two chords contain the same pitch classes (ignoring octave).

    Args:
        c1: First chord as a list of MIDI note numbers.
        c2: Second chord as a list of MIDI note numbers.

    Returns:
        True if both chords have the same pitch classes, False otherwise.

    Example:
        >>> is_same_chord([60, 64, 67], [72, 76, 79])  # Both C major
        True
        >>> is_same_chord([60, 64, 67], [60, 63, 67])  # C major vs C minor
        False
    """
    return {x % 12 for x in c1} == {x % 12 for x in c2}


def is_same_inversion(c1: List[int], c2: List[int]) -> bool:
    """
    Check if two chords have the same inversion (same bass note pitch class).

    Compares chords position by position to check if corresponding notes
    have the same pitch class.

    Args:
        c1: First chord as a list of MIDI note numbers.
        c2: Second chord as a list of MIDI note numbers.

    Returns:
        True if chords have matching pitch classes in order, False otherwise.

    Example:
        >>> is_same_inversion([60, 64, 67], [72, 76, 79])  # Same inversion
        True
        >>> is_same_inversion([60, 64, 67], [64, 67, 72])  # Different inversion
        False
    """
    return all(x1 % 12 == x2 % 12 for x1, x2 in zip(c1, c2))


def get_chord_from_notes(notes_as_list: Set[int]) -> Dict[str, List[int]]:
    """
    Identify possible chord names from a set of notes.

    Analyzes a set of MIDI notes and returns all matching chord types
    from the chord dictionary.

    Args:
        notes_as_list: A set of MIDI note numbers to analyze.

    Returns:
        A dictionary mapping chord names (e.g., "C5 major") to their
        MIDI note representations.

    Example:
        >>> get_chord_from_notes({60, 64, 67})
        {'C5 major': [60, 64, 67]}
    """
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
    """
    Calculate the mean pitch distance between two chords by type.

    Computes the absolute difference between the average pitch of each chord.
    Useful for finding chords in similar registers.

    Args:
        base_note: Root note of the first chord.
        chord_type: Type of the first chord.
        base_note2: Root note of the second chord.
        chord_type2: Type of the second chord.
        inversion: Inversion of the first chord.
        inversion2: Inversion of the second chord.

    Returns:
        The absolute difference between mean pitches of the two chords.

    Example:
        >>> get_mean_chord_distance("C5", "major", "G5", "major")
        7.0
    """
    return get_mean_chord_distance_chord(get_chord(base_note, chord_type, inversion),
                                         get_chord(base_note2, chord_type2, inversion2))


def get_mean_chord_distance_chord(chord1: List[int], chord2: List[int]) -> float:
    """
    Calculate the mean pitch distance between two chord note lists.

    Args:
        chord1: First chord as a list of MIDI note numbers.
        chord2: Second chord as a list of MIDI note numbers.

    Returns:
        The absolute difference between the average pitch of each chord.

    Example:
        >>> get_mean_chord_distance_chord([60, 64, 67], [67, 71, 74])
        7.0
    """
    return abs(sum(chord1) / len(chord1) - sum(chord2) / len(chord2))


def get_taxicab_chord_distance_chord(chord1: List[int], chord2: List[int]) -> float:
    """
    Calculate the taxicab (Manhattan) distance between two chords.

    Computes the sum of absolute differences between corresponding chord tones.
    This metric is excellent for voice leading as it measures the total
    movement required for all voices.

    Args:
        chord1: First chord as a list of MIDI note numbers.
        chord2: Second chord as a list of MIDI note numbers.

    Returns:
        The minimum taxicab distance, trying different alignments if chords
        have different lengths.

    Example:
        >>> get_taxicab_chord_distance_chord([60, 64, 67], [62, 65, 69])
        6  # Each voice moves by 2 semitones
    """
    if len(chord1) > len(chord2):
        return get_taxicab_chord_distance_chord(chord2, chord1)
    c1 = sorted(chord1)
    c2 = sorted(chord2)
    delta_l = len(c2) - len(c1)
    dist = 10000
    for i in range(delta_l + 1):
        dist = min(dist, sum(abs(c2[i + j] - c1[j]) for j in range(len(c1))))
    return dist


def get_taxicab_chord_distance(base_note: Union[int, str], chord_type, base_note2: Union[int, str], chord_type2,
                               inversion=0, inversion2=0) -> float:
    """
    Calculate the taxicab distance between two chords by type.

    Args:
        base_note: Root note of the first chord.
        chord_type: Type of the first chord.
        base_note2: Root note of the second chord.
        chord_type2: Type of the second chord.
        inversion: Inversion of the first chord.
        inversion2: Inversion of the second chord.

    Returns:
        The taxicab distance between the two chords.

    Example:
        >>> get_taxicab_chord_distance("C5", "major", "D5", "minor")
        6
    """
    return get_taxicab_chord_distance_chord(get_chord(base_note, chord_type, inversion),
                                            get_chord(base_note2, chord_type2, inversion2))


def get_closest_inversion(base_note: Union[int, str], chord_type, base_note2: Union[int, str], chord_type2,
                          inversion) -> List[int]:
    """
    Find the inversion of chord2 closest to chord1 using mean distance.

    Searches through all inversions of the second chord to find the one
    with the smallest mean pitch distance from the first chord.

    Args:
        base_note: Root note of the first chord.
        chord_type: Type of the first chord.
        base_note2: Root note of the second chord.
        chord_type2: Type of the second chord.
        inversion: Inversion of the first chord.

    Returns:
        The second chord in its closest inversion as a list of MIDI notes.

    Example:
        >>> get_closest_inversion("C5", "major", "G5", "major", 0)
        [67, 71, 74]  # G major in root position (closest to C major)
    """
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
    """
    Find the voicing of chord2 with minimal voice movement from chord1.

    Uses taxicab distance to find the voicing that requires the least
    total voice movement, ideal for smooth voice leading.

    Args:
        base_note: Root note of the first chord.
        chord_type: Type of the first chord.
        base_note2: Root note of the second chord.
        chord_type2: Type of the second chord.
        inversion: Inversion of the first chord.

    Returns:
        The second chord in its optimal voicing for voice leading.

    Example:
        >>> get_closest_taxicab_inversion("C5", "major", "F5", "major", 0)
        # Returns F major voicing with minimal voice movement from C major
    """
    chord_two_possibilities = get_inversion_unfiltered(get_chord(get_transpose_num(base_note2, -12), chord_type2), 3)
    chord_one = get_chord(base_note, chord_type, inversion)
    return min(chord_two_possibilities, key=lambda chord_two: get_taxicab_chord_distance_chord(chord_one, chord_two))


def get_closest_taxicab_inversion_chord(chord_one: List[int], chord_2: List[int]) -> List[int]:
    """
    Find the voicing of chord_2 with minimal voice movement from chord_one.

    Takes chord lists directly instead of chord specifications.
    Useful when working with already-constructed chords.

    Args:
        chord_one: First chord as a list of MIDI note numbers.
        chord_2: Second chord as a list of MIDI note numbers.

    Returns:
        A voicing of chord_2 with minimal taxicab distance from chord_one.

    Example:
        >>> get_closest_taxicab_inversion_chord([60, 64, 67], [65, 69, 72])
        # Returns F major voicing closest to the given C major voicing
    """
    chord_two_possibilities = get_inversion_unfiltered([get_transpose_num(note, -12) for note in chord_2], 3)
    return min(chord_two_possibilities, key=lambda chord_two: get_taxicab_chord_distance_chord(chord_one, chord_two))
