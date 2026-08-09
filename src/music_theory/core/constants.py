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
    # Triads
    'maj': ['unison', 'major_third', 'perfect_fifth'],
    'm': ['unison', 'minor_third', 'perfect_fifth'],
    'dim': ['unison', 'minor_third', 'tritone'],
    'aug': ['unison', 'major_third', 'minor_sixth'],

    # Suspended
    'sus2': ['unison', 'major_second', 'perfect_fifth'],
    'sus4': ['unison', 'perfect_fourth', 'perfect_fifth'],

    # Sixths
    '6': ['unison', 'major_third', 'perfect_fifth', 'major_sixth'],
    'm6': ['unison', 'minor_third', 'perfect_fifth', 'major_sixth'],
    '6/9': [
        'unison', 'major_second', 'major_third',
        'perfect_fifth', 'major_sixth', 'major_ninth'
    ],

    # Sevenths
    '7': ['unison', 'major_third', 'perfect_fifth', 'minor_seventh'],
    'maj7': ['unison', 'major_third', 'perfect_fifth', 'major_seventh'],
    'm7': ['unison', 'minor_third', 'perfect_fifth', 'minor_seventh'],
    'mMaj7': ['unison', 'minor_third', 'perfect_fifth', 'major_seventh'],
    'dim7': ['unison', 'minor_third', 'tritone', 'major_sixth'],
    'm7b5': ['unison', 'minor_third', 'tritone', 'minor_seventh'],

    # Altered sevenths
    '7b5': ['unison', 'major_third', 'tritone', 'minor_seventh'],
    '7#5': ['unison', 'major_third', 'minor_sixth', 'minor_seventh'],
    '7b9': [
        'unison', 'major_third', 'perfect_fifth',
        'minor_seventh', 'minor_ninth'
    ],
    '7#9': [
        'unison', 'major_third', 'perfect_fifth',
        'minor_seventh', 'minor_third'
    ],

    'maj7b5': ['unison', 'major_third', 'tritone', 'major_seventh'],
    'maj7#5': ['unison', 'major_third', 'minor_sixth', 'major_seventh'],
    'm7#5': ['unison', 'minor_third', 'minor_sixth', 'minor_seventh'],

    # Suspended sevenths
    '7sus2': ['unison', 'major_second', 'perfect_fifth', 'minor_seventh'],
    '7sus4': ['unison', 'perfect_fourth', 'perfect_fifth', 'minor_seventh'],

    # Ninths
    'add9': [
        'unison', 'major_second', 'major_third',
        'perfect_fifth', 'major_ninth'
    ],
    '9': [
        'unison', 'major_third', 'perfect_fifth',
        'minor_seventh', 'major_ninth'
    ],
    'maj9': [
        'unison', 'major_third', 'perfect_fifth',
        'major_seventh', 'major_ninth'
    ],
    'm9': [
        'unison', 'minor_third', 'perfect_fifth',
        'minor_seventh', 'major_ninth'
    ],
    'mMaj9': [
        'unison', 'minor_third', 'perfect_fifth',
        'major_seventh', 'major_ninth'
    ],
    'sus9': [
        'unison', 'major_second', 'perfect_fifth', 'major_ninth'
    ],
    '9sus4': [
        'unison', 'perfect_fourth', 'perfect_fifth',
        'minor_seventh', 'major_ninth'
    ],

    # Elevenths
    'm11': [
        'unison', 'minor_third', 'perfect_fifth',
        'minor_seventh', 'major_ninth', 'minor_eleventh'
    ],
    'maj11': [
        'unison', 'major_third', 'perfect_fifth',
        'major_seventh', 'major_ninth', 'major_eleventh'
    ],
    '11': [
        'unison', 'major_third', 'perfect_fifth',
        'minor_seventh', 'major_ninth', 'major_eleventh'
    ],

    # Thirteenths
    'm13': [
        'unison', 'minor_third', 'perfect_fifth',
        'minor_seventh', 'major_ninth', 'major_thirteenth'
    ],
    'maj13': [
        'unison', 'major_third', 'perfect_fifth',
        'major_seventh', 'major_ninth', 'major_thirteenth'
    ],
    '13': [
        'unison', 'major_third', 'perfect_fifth',
        'minor_seventh', 'major_ninth', 'major_thirteenth'
    ],
}

min_note = 0
max_note = 120
middle_octave = 4