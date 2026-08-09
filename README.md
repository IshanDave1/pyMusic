# pyMusic

A Python music composition and theory library for creating MIDI files with chord progressions, arpeggios, raga melodies, and guitar synthesis. Focus on music theory, voice leading, and Indian classical music (raga) generation.

## Features

- **Chord Progressions**: Build multi-section chord progressions with smooth voice leading
- **Chord Voicing**: Advanced inversions, openness control, and octave doubling
- **Arpeggio Generation**: Generate arpeggiated chord patterns with customizable timing
- **Raga Melodies**: Generate melodies following Indian classical music (raag) rules
- **Guitar Synthesis**: Synthesize guitar strumming patterns with realistic voicing
- **MIDI Output**: All generators output playable MIDI files
- **Voice Leading**: Smooth voice leading between chords with minimal note movement

## Project Structure

```
pyMusic/
├── src/music_theory/           # Main library
│   ├── core/
│   │   ├── notes.py            # Note/chord building and manipulation
│   │   ├── chord.py            # Chord analysis utilities
│   │   └── constants.py        # Musical definitions (notes, scales, chords)
│   ├── midi/
│   │   ├── compose.py          # Chord progression MIDI generation (multi-section support)
│   │   └── arpeggio.py         # Arpeggio pattern MIDI generation
│   ├── guitar/
│   │   ├── guitar_chord.py     # Guitar chord utilities and tablature
│   │   └── synthesizer.py      # Guitar strumming synthesis
│   └── raga/
│       └── raga_generator.py   # Indian classical melody generation
├── scripts/                    # Standalone executable programs
│   ├── compose_chords.py       # Generate chord progressions (configurable sections)
│   ├── generate_arpeggios.py   # Generate arpeggiated chords
│   ├── generate_raga.py        # Generate raga melodies
│   └── synthesize_guitar.py    # Generate guitar strumming MIDI
├── tests/                      # Test suite
├── outputs/                    # Generated MIDI files (default output location)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Quick Start

### Installation

1. Clone the repository and install dependencies:

```bash
git clone https://github.com/IshanDave1/pyMusic.git
cd pyMusic
pip install -r requirements.txt
```

2. Run any of the 4 simple scripts to generate MIDI:

```bash
cd scripts
python compose_chords.py       # Generate chord progressions
python generate_arpeggios.py   # Generate arpeggiated chords
python generate_raga.py        # Generate raga melodies
python synthesize_guitar.py    # Generate guitar strumming
```

All output MIDI files are saved to `../outputs/`

### Using the Scripts

Each script is a standalone program with easy configuration at the top:

#### compose_chords.py
Generate chord progressions with multiple sections, smooth voice leading, and custom patterns.

```python
# Define sections with chords, durations, patterns, and loop count
SECTIONS = [
    (
        ["C", "G:7", "F"],  # Chords; omitted quality means major
        [4, 4, 4],  # Duration (quarter notes)
        [[1, 1], [1, 1], [1]],  # Patterns (optional)
        2,  # Loop count
    ),
]

SMOOTH_VOICING = True  # Enable smooth voice leading
```

**Chord Format**: Chords use `ROOT[:QUALITY]`; omitted quality means major:
- Simple: `"C4"`
- Minor/named quality: `"C4:m"`
- Extended quality: `"C4:maj7"`
- Voicing: `ChordEvent("C4:maj7", inversion=1, openness=0.3)`

#### generate_arpeggios.py
Generate arpeggiated chord patterns with configurable strumming direction and spacing.

```python
CHORDS = ["C4", "G4", "A4:m"]
PATTERN = [1, 2, 1]  # How many times to repeat each chord
STRUM_DIRECTION = "down"  # or "up" or "alternating"
```

#### generate_raga.py
Generate melodies following Indian classical music (raag) rules.

```python
RAAG = "yaman"  # Choose from predefined raags
LENGTH = 256  # Melody length in note indices
TEMPO = 180
```

#### synthesize_guitar.py
Generate guitar strumming with realistic note voicing and patterns.

```python
GUITAR_CHORDS = [
    [0, 0, 2, 2, 1, 0],  # Chord tab (fret positions per string)
    [-1, 0, 2, 2, 1, 0],
]
PATTERN = GuitarChordPattern.downstrokes_4_16th()  # Predefined patterns
```

## Library API

### compose.py - Chord Progression Generation

```python
from src.music_theory.midi.compose import compose_chord_progression
from src.music_theory.core.chord import ChordEvent

sections = [
    (["C", "F", "G"], [4, 4, 4], None, 1),
]

compose_chord_progression(
    sections,
    output_file="output.mid",
    tempo=120,
    volume=70,
    smooth_voicing=True,  # Apply voice leading between chords
    verbose=True,
)
```

**Multi-Section Support**: Each section has its own:
- Chord list
- Per-chord durations (quarter notes)
- Per-chord patterns (for arpeggiation/rhythmic control)
- Loop count (how many times to repeat the section)

**Smooth Voice Leading**: When enabled, chords are re-voiced to minimize note movement, creating natural-sounding progressions. Voice leading persists across section boundaries and loops back to the first chord for seamless cycling.

### notes.py - Chord Building

```python
from src.music_theory.core.notes import build_chord, find_chord_voicing_by_common_tones

# Build a chord with various options
chord = build_chord("C4")  # [60, 64, 67]
inverted = build_chord("C4", inversion=1)  # [64, 67, 72]
open = build_chord("C4", openness=0.5)  # Wider voicing

# Smart voice leading
voicing = find_chord_voicing_by_common_tones(
    chord1=[60, 64, 67], chord2=[65, 69, 72]
)  # Returns chord2 re-voiced closest to chord1
```

### arpeggio.py - Arpeggio Generation

```python
from src.music_theory.midi.arpeggio import generate_arpeggio_progression

chords = ["C4", "G4"]
patterns = [2, 3]  # Repeat times
strum = "down"

generate_arpeggio_progression(
    chords, output_file="output.mid", patterns=patterns, strum_direction=strum
)
```

### raga_generator.py - Raga Melody Generation

```python
from src.music_theory.raga.raga_generator import generate_raga_melody_prog

generate_raga_melody_prog(
    raag_name="bhairav", length=128, output_file="raga.mid", tempo=180, volume=70
)
```

### synthesizer.py - Guitar Synthesis

```python
from src.music_theory.guitar.synthesizer import synthesize_guitar_progression

guitar_chords = [[0, 0, 2, 2, 1, 0], [0, 0, 0, 2, 1, 0]]
patterns = [4, 4]  # Repeat times per chord

synthesize_guitar_progression(
    guitar_chords, output_file="guitar.mid", patterns=patterns, pattern_type="downstrokes"
)
```

## Supported Musical Elements

### Scales
- `major`, `minor`, `harmonic_minor`, `melodic_minor`
- Modes: `dorian`, `phrygian`, `lydian`, `mixolydian`, `aeolian`, `locrian`
- Pentatonic: `major_pentatonic`, `minor_pentatonic`
- Blues: `major_blues`, `minor_blues`

### Chords
- Triads: `maj`, `m`, `dim`, `aug`, `sus2`, `sus4`
- Sevenths: `7`, `maj7`, `m7`, `mMaj7`, `dim7`, `m7b5`
- Extended: `9`, `maj9`, `m9`, `mMaj9`, `11`, `maj11`, `m11`, `13`, `maj13`, `m13`
- Other: `add9`, `6`, `m6`, `6/9`, `sus9`, `9sus4`, and more

### Raag System (Indian Classical Music)
- Bhairav, Yaman, Kafi, Bhimpalasi, Khamaj, Marwa, and others
- Each raag has specific ascending/descending scale patterns and characteristic phrases

## Note Naming Convention

- Format: `[Note][Accidental][Octave]`
- Sharps: use 's' (e.g., `Cs`, `Fs`, `Gs`)
- Flats: use 'b' (e.g., `Db` = `Cs`)
- Octave: 0-8 (default is 4 if omitted)
- Examples: `C4` (middle C = MIDI 60), `Fs3` (F# in octave 3), `G2`, `As5`

## Testing

Run the test suite:

```bash
python -m pytest tests/

# Or specific tests:
python tests/test_raga_generator.py
python tests/chord_progression_test.py
```

## Dependencies

- `midiutil` (==1.2.1) - MIDI file creation
- `numpy` (optional) - Advanced numerical operations

See `requirements.txt` for exact versions.

## Key Concepts

### Voice Leading
The library implements smooth voice leading to create natural-sounding chord transitions by minimizing the distance notes move between consecutive chords. This is especially useful for jazz progressions and complex voicings.

### Chord Voicing Options
- **Inversion**: Change which note is at the bottom (0 = root, 1 = first inversion, etc.)
- **Octave**: Double specific notes in different octaves
- **Openness**: Control how spread out the chord is (0 = close, 1 = very open)

### Patterns
Control how chords are played:
- `[1]` - play chord once for full duration
- `[2, 2]` - split duration in half, play chord twice
- `[3, 3, 2]` - play 3/8, 3/8, 2/8 of duration proportionally

## Examples

### Jazz 2-5-1 Progression with Smooth Voicing

```python
from src.music_theory.midi.compose import compose_chord_progression

sections = [
    (
        [
            "D4:m7",  # ii chord
            "G4:7",  # V chord
            "C4:maj7",  # I chord
        ],
        [4, 4, 4],
        None,
        2,  # Loop twice
    ),
]

compose_chord_progression(
    sections, output_file="jazz_251.mid", tempo=140, volume=80, smooth_voicing=True
)
```

### Raga Improvisation

```python
from src.music_theory.raga.raga_generator import generate_raga_melody_prog

generate_raga_melody_prog(
    raag_name="bhairav", length=256, output_file="bhairav_improv.mid", tempo=180
)
```

## Contributing

This project welcomes contributions:
- Add new raag definitions
- Improve voice leading algorithms
- Add new chord voicing options
- Extend guitar tuning systems
- Add more strum patterns

## License

[Add appropriate license here]

## References

- MIDI Specification: https://www.midi.org/
- Music Theory: https://en.wikipedia.org/wiki/Music_theory
- Indian Classical Music: https://en.wikipedia.org/wiki/Indian_classical_music
- Voice Leading: https://en.wikipedia.org/wiki/Voice_leading
