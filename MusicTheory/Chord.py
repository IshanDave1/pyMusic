"""
Chord module for generating chord progressions and arpeggios.

This module provides tools for creating chord progressions based on scale degrees,
with support for inversions, modal interchange, and custom chord voicings.
It also includes utilities for arpeggiating chords with custom patterns.
"""

from MusicTheory.Notes import get_scale_num, get_note


class ScaledChordProgression:
    """
    A class for generating chord progressions within a given scale.

    This class allows creation of chord progressions by specifying scale degrees,
    chord types (voicings), and supports inversions and modal interchange (borrowing
    chords from parallel scales).

    Attributes:
        base_note (int): The root note of the scale as a MIDI note number.
                         Default is 60 (middle C).

    Example:
        >>> scp = ScaledChordProgression(48)  # C3 as base
        >>> cp = scp.gp([1, 4, 5, 1], "major")  # I-IV-V-I progression
    """

    def __init__(self, base_note=60):
        """
        Initialize a ScaledChordProgression with a base note.

        Args:
            base_note (int): The root note of the scale as a MIDI note number.
                             Default is 60 (middle C). Common values:
                             - 48 = C3
                             - 60 = C4 (middle C)
                             - 72 = C5
        """
        self.base_note = base_note

    def gp(self, degrees, scale_type="major", chord_types=None):
        """
        Generate a chord progression based on scale degrees.

        Creates chords from the specified scale degrees with optional inversions,
        custom voicings, and modal interchange.

        Args:
            degrees (list): A list of scale degrees. Each element can be:
                - int: A scale degree (1-based). E.g., 1 for tonic, 5 for dominant.
                - tuple(int, int): (degree, inversion). Inversion shifts which chord
                  tone is in the bass. E.g., (4, 1) is the IV chord, first inversion.
                - tuple(int, int, str): (degree, inversion, mode). Borrows a chord
                  from a parallel scale. E.g., (4, 0, "minor") borrows iv from
                  the parallel minor.
            scale_type (str): The scale type to use. Default is "major".
                              Must be a valid scale type recognized by get_scale_num().
            chord_types (list[list[int]] | None): Optional list of chord voicings,
                one per degree. Each voicing is a list of 1-based scale intervals.
                Default is [[1, 3, 5], ...] (triads) for each degree.
                Examples:
                - [1, 3, 5] = triad (root, 3rd, 5th)
                - [1, 3, 5, 7] = seventh chord
                - [0, 2, 4, 6] = same as [1, 3, 5, 7] (0-indexed internally)

        Returns:
            list[list[int]]: A list of chords, where each chord is a list of
                             MIDI note numbers.

        Example:
            >>> scp = ScaledChordProgression(48)
            >>> # I-IV(1st inv)-vi-V progression with 7th chords
            >>> cp = scp.gp([1, (4, 1), 6, 5], "major", [[1,3,5,7]]*4)
        """
        print(degrees)
        if chord_types is None:
            chord_types = [[1, 3, 5] for _ in range(len(degrees))]

        # Make a deep copy to avoid mutating the caller's list
        chord_types = [list(ct) for ct in chord_types]

        for chord_type in chord_types:
            for note_index in range(len(chord_type)):
                chord_type[note_index] = chord_type[note_index] - 1

        scale_notes = get_scale_num(self.base_note, scale_type)
        scale_notes = scale_notes + [x + 12 for x in scale_notes] + [x + 24 for x in scale_notes]
        print([get_note(x) for x in scale_notes])
        print(scale_notes)

        cp = []
        for i in range(len(degrees)):
            degree = degrees[i]
            chord_type = chord_types[i]
            if type(degree) == int:
                start_note = degree - 1
                chord = [scale_notes[start_note + x] for x in (chord_type + [y + 7 for y in chord_type])[0:len(chord_type)]]
                cp.append(chord)
            elif type(degree) == tuple and len(degree) == 2:
                start_note = degree[0] - 1
                inversion = degree[1]
                chord = [scale_notes[start_note + x] for x in
                         (chord_type + [y + 7 for y in chord_type])[inversion:inversion + len(chord_type)]]
                cp.append(chord)
            else:
                start_note = degree[0] - 1
                inversion = degree[1]
                mode = degree[2]
                parallel_scale_notes = get_scale_num(self.base_note, mode)
                parallel_scale_notes = parallel_scale_notes + [x + 12 for x in parallel_scale_notes] + [x + 24 for x in
                                                                                                        parallel_scale_notes]
                chord = [parallel_scale_notes[start_note + x] for x in
                         (chord_type + [y + 7 for y in chord_type])[inversion:inversion + len(chord_type)]]
                cp.append(chord)
            # print(chord)

        return cp


def arpeggiate_chord(chord, length, pattern=None):
    """
    Generate an arpeggiated sequence from a chord.

    Takes a chord and creates a sequence of individual notes based on a pattern,
    spanning multiple octaves.

    Args:
        chord (list[int]): A list of MIDI note numbers representing the chord.
        length (int): The desired length of the output arpeggio sequence.
        pattern (list[int] | None): Optional list of indices specifying the order
            to play chord tones. Indices refer to positions in the extended chord
            (original + 1 octave up + 2 octaves up). If None, defaults to sequential
            order [0, 1, 2, ...] through all chord tones.

    Returns:
        list[int]: A list of MIDI note numbers representing the arpeggiated sequence.

    Raises:
        AssertionError: If any pattern index exceeds the extended chord length.

    Example:
        >>> chord = [60, 64, 67]  # C major triad
        >>> arp = arpeggiate_chord(chord, 16, [0, 1, 3, 2, 0, 1, 2, 3])
        >>> # Returns a 16-note arpeggio following the specified pattern
    """
    chord = chord + [x + 12 for x in chord] + [x + 24 for x in chord]
    if pattern is None:
        pattern = [i for i in range(len(chord))]
    pattern *= 5
    # print(progression,length,pattern)
    arp = [0 for _ in range(length)]
    assert all(x < len(chord) for x in pattern)
    for i in range(length):
        arp[i] = chord[pattern[(i)]]

    return arp
