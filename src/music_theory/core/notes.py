"""
Notes module for music theory operations.

This module provides comprehensive utilities for working with musical notes,
scales, chords, and voice leading. It supports MIDI note numbers and string
representations (e.g., "C4", "Fs3") and includes functions for transposition,
scale generation, chord construction with advanced voicing options, and
finding optimal chord inversions for smooth voice leading.

Note naming convention:
    - Notes are named A-G with 's' suffix for sharps (e.g., Cs, Fs, Gs)
    - Octave numbers follow standard MIDI convention
    - MIDI note 60 = C4 (middle C)
    - Default octave (when not specified) is 4, so "C" = C4 = MIDI 60
"""

import math
from itertools import product
from typing import List, Union, Set, Dict

from src.music_theory.core.constants import *


def note_to_midi(note: Union[int, str]) -> int:
    """Convert note to MIDI number if it's a string."""
    if isinstance(note, str):
        return note_string_to_midi(note)
    return note


def extend_notes_across_octaves(notes: List[int], octaves: int = 3) -> List[int]:
    """Extend a list of notes across multiple octaves.
    
    Args:
        notes: List of MIDI note numbers.
        octaves: Number of octaves to span (default 3).
    
    Returns:
        Extended list with notes repeated at higher octaves.
    """
    result = []
    for i in range(octaves):
        result.extend([n + 12 * i for n in notes])
    return result


def note_string_to_midi(note: str) -> int:
    """
    Convert a note string to its MIDI note number.

    Args:
        note: A note string in format "NoteName" or "NoteNameOctave".
              Examples: "C", "C4", "Fs3", "Gs"
              If no octave is specified, uses middle_octave from constants.

    Returns:
        The MIDI note number (0-127 range typically).

    Raises:
        ValueError: If the note string is invalid.

    Examples:
        >>> note_string_to_midi("C4")
        60
        >>> note_string_to_midi("Fs3")
        54
        >>> note_string_to_midi("C")  # Uses middle_octave default (4)
        60
    """
    if any(n.lower() == note.lower() for n in notes):
        return [n.lower() == note.lower() for n in notes].index(True) + (middle_octave + 1) * 12
    elif note[-1].isdigit() and any(n.lower() == note[:-1].lower() for n in notes):
        return [n.lower() == note[:-1].lower() for n in notes].index(True) + (int(note[-1]) + 1) * 12
    else:
        raise ValueError(
            f"Invalid note '{note}'. Notes must be A-G (with optional sharp 's' suffix: Cs, Ds, Fs, Gs, As) followed by an octave number.")


def midi_to_note_string(num: int) -> str:
    """
    Convert a MIDI note number to its string representation.

    Args:
        num: MIDI note number (must be within min_note to max_note range).

    Returns:
        Note string in format "NoteNameOctave" (e.g., "C4", "Fs3").

    Raises:
        ValueError: If num is outside the valid range.

    Examples:
        >>> midi_to_note_string(60)
        'C4'
        >>> midi_to_note_string(48)
        'C3'
    """
    if num < min_note or num > max_note:
        raise ValueError(f"num {num} has to be in range 0-100")
    return f"{notes[num % 12]}{num // 12 - 1}"


def transpose_note_to_string(note: Union[int, str], semitones: int = 12) -> str:
    """
    Transpose a note by a number of semitones and return as string.

    Args:
        note: The note to transpose (MIDI number or string like "C4").
        semitones: Number of semitones to transpose. Default is 12 (one octave up).
                   Negative values transpose down.

    Returns:
        The transposed note as a string.

    Examples:
        >>> transpose_note_to_string("C4")
        'C5'
        >>> transpose_note_to_string("C4", -12)
        'C3'
        >>> transpose_note_to_string(60, 7)
        'G4'
    """
    return midi_to_note_string(note_to_midi(note) + semitones)


def transpose_to_midi(note: Union[int, str], semitones: int = 12) -> int:
    """
    Transpose a note by a number of semitones and return as MIDI number.

    Args:
        note: The note to transpose (MIDI number or string like "C4").
        semitones: Number of semitones to transpose. Default is 12 (one octave up).
                   Negative values transpose down.

    Returns:
        The transposed note as a MIDI number.

    Examples:
        >>> transpose_to_midi("C4")
        72
        >>> transpose_to_midi(60, -12)
        48
    """
    return note_to_midi(note) + semitones


def build_scale_midi(num: Union[int, str], scale_type: str) -> List[int]:
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
        >>> build_scale_midi(60, "major")
        [60, 62, 64, 65, 67, 69, 71]
        >>> build_scale_midi("C4", "minor")
        [60, 62, 63, 65, 67, 68, 70]
    """
    if scale_type not in scales.keys():
        raise ValueError(f"not supported scale {scale_type}")
    num = note_to_midi(num)
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
        >>> get_scale_degree("C4", "major", 5)  # The 5th degree (G)
        67
        >>> get_scale_degree(60, "major", 3)  # The 3rd degree (E)
        64
    """
    return build_scale_midi(note, scale_type)[degree - 1]


def build_diatonic_chord(note: Union[int, str], scale_type: str, degree: int, num_notes: int) -> List[int]:
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
        >>> build_diatonic_chord("C4", "major", 1, 3)  # C major triad
        [60, 64, 67]
        >>> build_diatonic_chord("C4", "major", 2, 4)  # Dm7
        [62, 65, 69, 72]
    """
    base_scale = build_scale_midi(note, scale_type)
    scale = extend_notes_across_octaves(base_scale, 3)
    c_notes = [degree - 1 + 2 * i for i in range(num_notes)]
    return [scale[c_note] for c_note in c_notes]


def build_scale_note_strings(num: Union[int, str], scale_type: str) -> List[str]:
    """
    Generate a scale as a list of note name strings.

    Args:
        num: The root note of the scale (MIDI number or string).
        scale_type: The type of scale (e.g., "major", "minor", "dorian").

    Returns:
        A list of note strings representing the scale.

    Examples:
        >>> build_scale_note_strings(60, "major")
        ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
    """
    return [midi_to_note_string(n) for n in build_scale_midi(num, scale_type)]


def build_chord(base_note: Union[int, str], chord_type: str, inversion: int = 0, lower_octave_doubles: List[int] = None,
              upper_octave_doubles: List[int] = None, over_octaves=1,
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
        lower_octave_doubles: List of chord tone indices to double in the lower octave.
        upper_octave_doubles: List of chord tone indices to double in the upper octave.
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
        >>> build_chord("C4", "major")
        [60, 64, 67]
        >>> build_chord(60, "major", inversion=1)
        [64, 67, 72]
        >>> build_chord("C4", "major_seventh")
        [60, 64, 67, 71]
    """
    if interval_half_steps[chords[chord_type][-1]] > 12:
        over_octaves = max(over_octaves, 2)
    if openness < 0 or openness >= 1:
        raise ValueError(f"openness is {openness} it has to be in range [0,1)")
    if chord_type not in chords.keys():
        raise ValueError(f"not supported chord {chord_type}")
    base_note = note_to_midi(base_note)

    if lower_octave_doubles is None:
        lower_octave_doubles = []
    if upper_octave_doubles is None:
        upper_octave_doubles = []
    root_position = [base_note + interval_half_steps[interval] for interval in chords[chord_type]]
    lower_notes = [transpose_to_midi(root_position[index], -12) for index in lower_octave_doubles]
    upper_notes = [transpose_to_midi(root_position[index]) for index in upper_octave_doubles]
    base_part = root_position[inversion:]
    transposed_part = [transpose_to_midi(note) for note in root_position][:inversion]
    base_part.extend(transposed_part)
    base_part.sort()

    all_inversions = list(filter(lambda x: have_same_inversion(x, base_part), generate_chord_voicings(base_part, over_octaves)))
    base_part = all_inversions[math.floor(openness * len(all_inversions))]
    base_part.extend(lower_notes)
    base_part.extend(upper_notes)

    return sorted(base_part)


def generate_chord_voicings(chord: List[int], octaves: int, filtered: bool = True) -> List[List[int]]:
    """
    Generate all possible voicings of a chord across multiple octaves.

    Creates all combinations of chord tones spread across the specified
    number of octaves, optionally filtered to ensure proper voice spacing,
    and sorted by evenness of voice distribution.

    Args:
        chord: A list of MIDI note numbers representing the chord.
        octaves: Number of octaves to spread voicings across.
        filtered: If True (default), filters to ensure the voicing spans
                  at least (octaves-1) * 12 semitones. If False, includes
                  all voicings including tightly-spaced ones.

    Returns:
        A list of chord voicings (each a list of MIDI notes), sorted by
        evenness of note spacing.

    Example:
        >>> chord = [60, 64, 67]  # C major
        >>> voicings = generate_chord_voicings(chord, 2)
        >>> # Returns various spread voicings of C major across 2 octaves
        >>> all_voicings = generate_chord_voicings(chord, 2, filtered=False)
        >>> # Returns all voicings including tightly-spaced ones
    """
    chord_in_octaves = [[note + 12 * octave for octave in range(octaves)] for note in chord]
    voicings = [list(combo) for combo in product(*chord_in_octaves)]

    def get_evenness(spacing_list):
        return math.prod(spacing_list[i] - spacing_list[i - 1] for i in range(1, len(spacing_list)))

    sorted_voicings = sorted([sorted(voicing) for voicing in voicings], key=get_evenness)
    
    if filtered:
        return [voicing for voicing in sorted_voicings if voicing[-1] - voicing[0] >= 12 * (octaves - 1)]
    return sorted_voicings

def build_chord_from_pattern(chord: List[int], pattern: List[int]):
    pattern_indices = [x - 1 for x in pattern]
    start_note = chord[pattern_indices[0]] - 12 if (chord[pattern_indices[0]] > chord[0]) else chord[pattern_indices[0]]
    chord_pattern = [start_note]
    for i in range(1, len(pattern_indices)):
        next_note = chord[pattern_indices[i]] % 12
        while next_note < chord_pattern[-1]:
            next_note += 12
        chord_pattern.append(next_note)
    return chord_pattern



def generate_all_chord_voicings(chord: List[int], octaves: int) -> List[List[int]]:
    """
    Generate all possible voicings of a chord without span filtering.

    This is a convenience wrapper around generate_chord_voicings with filtered=False.

    Args:
        chord: A list of MIDI note numbers representing the chord.
        octaves: Number of octaves to spread voicings across.

    Returns:
        A list of all chord voicings sorted by evenness of note spacing.

    Example:
        >>> chord = [60, 64, 67]
        >>> all_voicings = generate_all_chord_voicings(chord, 2)
    """
    return generate_chord_voicings(chord, octaves, filtered=False)


def are_same_pitch_classes(chord_1: List[int], chord_2: List[int]) -> bool:
    """
    Check if two chords contain the same pitch classes (ignoring octave).

    Args:
        chord_1: First chord as a list of MIDI note numbers.
        chord_2: Second chord as a list of MIDI note numbers.

    Returns:
        True if both chords have the same pitch classes, False otherwise.

    Example:
        >>> are_same_pitch_classes([60, 64, 67], [72, 76, 79])  # Both C major
        True
        >>> are_same_pitch_classes([60, 64, 67], [60, 63, 67])  # C major vs C minor
        False
    """
    return {x % 12 for x in chord_1} == {x % 12 for x in chord_2}


def have_same_inversion(chord_1: List[int], chord_2: List[int]) -> bool:
    """
    Check if two chords have the same inversion (same bass note pitch class).

    Compares chords position by position to check if corresponding notes
    have the same pitch class.

    Args:
        chord_1: First chord as a list of MIDI note numbers.
        chord_2: Second chord as a list of MIDI note numbers.

    Returns:
        True if chords have matching pitch classes in order, False otherwise.

    Example:
        >>> have_same_inversion([60, 64, 67], [72, 76, 79])  # Same inversion
        True
        >>> have_same_inversion([60, 64, 67], [64, 67, 72])  # Different inversion
        False
    """
    return all(x1 % 12 == x2 % 12 for x1, x2 in zip(chord_1, chord_2))


def identify_chords_from_notes(notes_as_list: Set[int]) -> Dict[str, List[int]]:
    """
    Identify possible chord names from a set of notes.

    Analyzes a set of MIDI notes and returns all matching chord types
    from the chord dictionary.

    Args:
        notes_as_list: A set of MIDI note numbers to analyze.

    Returns:
        A dictionary mapping chord names (e.g., "C4 major") to their
        MIDI note representations.

    Example:
        >>> identify_chords_from_notes({60, 64, 67})
        {'C4 major': [60, 64, 67]}
    """
    def is_in_set(chord_tones, note_set) -> bool:
        return all(x in note_set for x in chord_tones)

    all_chords = {}
    for note in notes_as_list:
        for chord_type in chords:
            chord_as_list = build_chord(note, chord_type)
            if is_in_set({x % 12 for x in chord_as_list}, {x % 12 for x in notes_as_list}):
                all_chords[f"{midi_to_note_string(note)} {chord_type}"] = chord_as_list

    return all_chords

def calculate_mean_chord_distance(base_note: Union[int, str], chord_type, base_note2: Union[int, str], chord_type2,
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
        >>> abs(calculate_mean_chord_distance("C4", "major", "G4", "major") - 7.0) < 0.001
        True
    """
    return calculate_mean_chord_distance_between_notes(build_chord(base_note, chord_type, inversion),
                                         build_chord(base_note2, chord_type2, inversion2))


def calculate_mean_chord_distance_between_notes(chord1: List[int], chord2: List[int]) -> float:
    """
    Calculate the mean pitch distance between two chord note lists.

    Args:
        chord1: First chord as a list of MIDI note numbers.
        chord2: Second chord as a list of MIDI note numbers.

    Returns:
        The absolute difference between the average pitch of each chord.

    Example:
        >>> abs(calculate_mean_chord_distance_between_notes([60, 64, 67], [67, 71, 74]) - 7.0) < 0.001
        True
    """
    return abs(sum(chord1) / len(chord1) - sum(chord2) / len(chord2))


def calculate_taxicab_distance_between_notes(chord1: List[int], chord2: List[int]) -> float:
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
        >>> calculate_taxicab_distance_between_notes([60, 64, 67], [62, 65, 69])
        5
    """
    if len(chord1) > len(chord2):
        return calculate_taxicab_distance_between_notes(chord2, chord1)
    c1 = sorted(chord1)
    c2 = sorted(chord2)
    delta_l = len(c2) - len(c1)
    dist = 10000
    for i in range(delta_l + 1):
        dist = min(dist, sum(abs(c2[i + j] - c1[j]) for j in range(len(c1))))
    return dist


def calculate_taxicab_distance(base_note: Union[int, str], chord_type, base_note2: Union[int, str], chord_type2,
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
        >>> calculate_taxicab_distance("C4", "major", "D4", "minor")
        5
    """
    return calculate_taxicab_distance_between_notes(build_chord(base_note, chord_type, inversion),
                                            build_chord(base_note2, chord_type2, inversion2))


def find_closest_chord_inversion_by_mean(base_note: Union[int, str], chord_type, base_note2: Union[int, str], chord_type2,
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
        >>> find_closest_chord_inversion_by_mean("C4", "major", "G4", "major", 0)
        [67, 71, 74]
    """
    return min(
        (
            (calculate_mean_chord_distance(
                base_note, chord_type, base_note2, chord_type2, inversion, inv
            ), build_chord(base_note2, chord_type2, inv))
            for inv in range(len(chords[chord_type2]))
        ),
        key=lambda x: x[0],
    )[1]


def find_closest_chord_voicing_for_voice_leading(base_note: Union[int, str], chord_type, base_note2: Union[int, str], chord_type2,
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
        >>> find_closest_chord_voicing_for_voice_leading("C4", "major", "F4", "major", 0)
        [60, 65, 69]
    """
    chord_two_possibilities = generate_all_chord_voicings(build_chord(transpose_to_midi(base_note2, -12), chord_type2), 3)
    chord_one = build_chord(base_note, chord_type, inversion)
    return min(chord_two_possibilities, key=lambda chord_two: calculate_taxicab_distance_between_notes(chord_one, chord_two))


def find_smooth_chord_voicing_from_notes(chord_one: List[int], chord_2: List[int]) -> List[int]:
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
        >>> find_smooth_chord_voicing_from_notes([60, 64, 67], [65, 69, 72])
        [60, 65, 69]
    """
    chord_two_possibilities = generate_all_chord_voicings([transpose_to_midi(note, -12) for note in chord_2], 3)
    return min(chord_two_possibilities, key=lambda chord_two: calculate_taxicab_distance_between_notes(chord_one, chord_two))

def find_chord_voicing_by_common_tones(chord1: List[int], chord2: List[int]) -> List[int]:
    """
    Find a voicing of chord2 that maintains common tones with chord1.
    
    This function preserves common pitch classes between chords in their original
    octaves from chord1, then places remaining notes in the octave closest to chord1.
    When multiple octaves have equal distance, prefers the closest register (octave offset
    closest to 0, i.e., keeping notes in their original octave).
    
    Args:
        chord1: List of MIDI note numbers for the reference chord
        chord2: List of MIDI note numbers for the chord to voice
    
    Returns:
        A sorted list of MIDI note numbers representing the voiced chord2
        
    Raises:
        ValueError: If either chord is empty
        
    Example:
        >>> find_chord_voicing_by_common_tones([60, 64, 67], [67, 71, 74])
        [59, 62, 67]  # G kept at 67, B and D placed close to chord1
    """
    # Input validation
    if not chord1 or not chord2:
        raise ValueError("Both chord1 and chord2 must be non-empty lists")
    
    chord2_inversion = []
    same_note_indices = set()  # Use set to track which chord2 indices already used (dedup)
    
    # Find common pitch classes
    for note1 in chord1:
        for j, note2 in enumerate(chord2):
            # Only add each chord2 note once (dedup fix)
            if j not in same_note_indices and note1 % 12 == note2 % 12:
                same_note_indices.add(j)
                chord2_inversion.append(note1)
                break  # Exit inner loop - this chord2 note is now used

    def distance_sum_absolute(note_list, target_note):
        return sum(abs(x - target_note) for x in note_list)

    # Place remaining notes
    for i, note in enumerate(chord2):
        if i not in same_note_indices:
            min_distance = float('inf')
            best_octave_offsets = []  # Collect all offsets with minimum distance
            
            # Find all octave offsets with minimum distance
            for octave_offset in range(-2, 3):
                distance = distance_sum_absolute(chord1, note + 12 * octave_offset)
                if distance < min_distance:
                    min_distance = distance
                    best_octave_offsets = [octave_offset]
                elif distance == min_distance:  # Collect ties
                    best_octave_offsets.append(octave_offset)
            
            # Prefer closest register (offset closest to 0)
            best_octave_offset = min(best_octave_offsets, key=lambda x: abs(x))
            chord2_inversion.append(note + 12 * best_octave_offset)

    chord2_inversion.sort()
    return chord2_inversion


