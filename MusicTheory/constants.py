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

min_note = 0
max_note = 120
middle_octave = 4