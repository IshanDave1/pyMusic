# pyMusic

A comprehensive Python music theory and composition library supporting Western classical theory, guitar utilities, and Indian classical music (raga) generation.

## Features

- **Music Theory Basics**: Build scales, chords, and perform voice leading analysis
- **Guitar Utilities**: Guitar tuning systems, chord tab support, and guitar synthesis
- **MIDI Composition**: Create and compose MIDI files with flexible note scheduling
- **Raga Generation**: Generate melodies based on Indian classical music raag system
- **Advanced Chord Voicing**: Support for inversions, open voicings, and custom doublings

## Project Structure

```
pyMusic/
├── src/
│   ├── music_theory/
│   │   ├── core/              # Core music theory (notes, chords, scales)
│   │   │   ├── constants.py   # Musical note and chord definitions
│   │   │   ├── Notes.py       # Note manipulation and chord building
│   │   │   └── Chord.py       # Chord analysis utilities
│   │   ├── guitar/            # Guitar-specific utilities
│   │   │   ├── guitar_chord.py
│   │   │   └── guitar_synthesizer.py
│   │   ├── midi/              # MIDI file generation
│   │   │   ├── midi_composer.py
│   │   │   ├── midi_strummer.py
│   │   │   └── midi_demo.py
│   │   └── raga/              # Indian classical music generation
│   │       └── raga_generator.py
│   └── converter/             # Format conversion utilities
├── tests/                     # Test suite
├── outputs/                   # Generated MIDI files
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

## Installation

### Prerequisites
- Python 3.8+

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd pyMusic
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Note Operations

```python
from src.music_theory.core.Notes import (
    note_string_to_midi,
    midi_to_note_string,
    build_scale_midi,
    build_chord
)

# Convert note names to MIDI numbers
c4_midi = note_string_to_midi("C4")      # Returns 60
d_sharp = note_string_to_midi("Ds3")     # Returns 51

# Convert MIDI numbers back to note names
note_name = midi_to_note_string(60)      # Returns "C4"

# Build scales
c_major = build_scale_midi("C4", "major")     # [60, 62, 64, 65, 67, 69, 71]
a_minor = build_scale_midi("A3", "minor")     # [57, 59, 60, 62, 64, 65, 67]

# Build chords
c_major_chord = build_chord("C4", "major")           # [60, 64, 67]
g_dominant7 = build_chord("G4", "dominant_seventh")  # [67, 71, 74, 76]

# Chord inversions
c_major_first_inv = build_chord("C4", "major", inversion=1)  # [64, 67, 72]
```

### Guitar Utilities

```python
from src.music_theory.guitar import get_chord_from_tabs, STANDARD_GUITAR_TUNING_MIDI

# Get chord from tablature
tabs = [0, 0, 2, 2, 1, 0]  # Capo positions for each string
chord_notes = get_chord_from_tabs(tabs)
```

### MIDI File Generation

```python
from src.music_theory.raga import generate_melody, melody_to_midi

# Generate a melody using Indian classical raga
melody = generate_melody(raag, length=32)

# Write to MIDI file
melody_to_midi(melody, "output.mid", tempo=180, volume=80)
```

### Raga Generation

```python
from src.music_theory.raga import generate_melody, melody_to_midi, raag

# Generate a melody
melody = generate_melody(raag, 128)

# Write to MIDI
melody_to_midi(melody, "raga_output.mid")
```

## Core Modules

### `music_theory.core.Notes`
Comprehensive note and chord manipulation utilities:
- `note_to_midi()` / `note_string_to_midi()` - Convert between note names and MIDI numbers
- `midi_to_note_string()` - Convert MIDI to note names
- `build_scale_midi()` - Generate scale notes
- `build_chord()` - Generate chords with voicing options
- `build_diatonic_chord()` - Build chords from scale degrees
- Voice leading helpers for smooth chord progressions

### `music_theory.core.constants`
Musical definitions:
- `notes` - Chromatic scale note names
- `scales` - Scale interval patterns (major, minor, modes, etc.)
- `chords` - Chord definitions (major, minor, seventh chords, etc.)
- `interval_half_steps` - Interval definitions

### `music_theory.guitar`
Guitar-specific utilities:
- `STANDARD_GUITAR_TUNING_MIDI` - Standard 6-string guitar tuning
- `get_chord_from_tabs()` - Convert tablature to chord notes

### `music_theory.midi`
MIDI file generation:
- `midi_composer` - MIDI composition utilities
- `midi_strummer` - Guitar strumming patterns for MIDI

### `music_theory.raga`
Indian classical music generation:
- `generate_melody()` - Generate melodies based on raag rules
- `melody_to_midi()` - Write melodies to MIDI files
- `get_note_at_index()` - Get notes from raag scales

## Testing

Run tests from the project root:

```bash
python -m pytest tests/
```

Or run specific test files:

```bash
python tests/test_raga_generator.py
python tests/chord_progression_test.py
```

## Dependencies

- `midiutil` - MIDI file creation
- `numpy` - Numerical operations (optional, for advanced features)

See `requirements.txt` for complete list with versions.

## API Reference

### Supported Scales
- `major`, `minor`, `harmonic_minor`
- Modal scales: `dorian`, `phrygian`, `lydian`, `mixolydian`, `aeolian`, `locrian`
- Pentatonic: `major_pentatonic`, `minor_pentatonic`
- Blues: `major_blues`, `minor_blues`

### Supported Chords
- Triads: `major`, `minor`, `diminished`, `augmented`, `sus2`, `sus4`
- Seventh chords: `major_seventh`, `minor_seventh`, `dominant_seventh`, `diminished_seventh`
- Extended chords: `major_ninth`, `minor_ninth`, `dominant_ninth`
- Other: `add9`, `6/9`, `sus9`, and many more

## Note Naming Convention

- Notes use A-G with 's' suffix for sharps (e.g., `Cs`, `Fs`, `Gs`)
- MIDI note 60 = C4 (middle C)
- Default octave is 4 when not specified
- Examples: `C4`, `Fs3`, `G2`, `As5`

## Contributing

This is an active music theory project. Feel free to:
- Add new scale or chord types
- Improve voice leading algorithms
- Expand raga definitions
- Add more guitar tuning systems

## License

[Add appropriate license here]

## References

- MIDI Specification: https://www.midi.org/
- Music Theory: https://en.wikipedia.org/wiki/Music_theory
- Indian Classical Music: https://en.wikipedia.org/wiki/Indian_classical_music
