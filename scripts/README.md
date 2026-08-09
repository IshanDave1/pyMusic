# Scripts

Executable scripts for generating MIDI files using the pyMusic library.

## Available Scripts

### `generate_raga_melody.py`

Generate Indian classical music melodies using raag patterns.

**Usage:**
```bash
./generate_raga_melody.py [OPTIONS]
python scripts/generate_raga_melody.py --length 256 --tempo 240
```

**Options:**
- `-l, --length`: Length of melody in notes (default: 128)
- `-o, --output`: Output MIDI file path (default: outputs/raga_melody.mid)
- `--tempo`: Tempo in BPM (default: 180)
- `--volume`: MIDI volume 0-127 (default: 48)
- `--beat-duration`: Beats per whole note (default: 4)

**Examples:**
```bash
# Generate simple 128-note melody
python scripts/generate_raga_melody.py

# Generate longer melody with custom tempo
python scripts/generate_raga_melody.py --length 512 --tempo 240 --volume 80

# Output to custom location
python scripts/generate_raga_melody.py -o my_raga.mid --length 256
```

---

### `compose_chord_progression.py`

Compose chord progressions with smooth voice leading.

**Usage:**
```bash
./compose_chord_progression.py [OPTIONS] CHORD [CHORD ...]
python scripts/compose_chord_progression.py Gs3:m E3:maj G3:maj B3:maj
```

**Arguments:**
- `CHORDS`: Chord sequence as `Note:ChordType` (e.g., `C4:maj`, `F3:m7`)

**Options:**
- `-o, --output`: Output MIDI file path (default: outputs/chord_progression.mid)
- `--tempo`: Tempo in BPM (default: 115)
- `--volume`: MIDI volume 0-127 (default: 48)
- `--duration`: Duration of each chord in beats (default: 4)

**Examples:**
```bash
# Compose a simple progression
python scripts/compose_chord_progression.py Gs3:m E3:maj G3:maj B3:maj

# Custom output and tempo
python scripts/compose_chord_progression.py \
  -o my_progression.mid --tempo 140 --volume 60 \
  Gs3:m E3:maj G3:maj B3:maj

# Extended progression with sevenths
python scripts/compose_chord_progression.py \
  E3:maj7 E3:maj G3:maj B3:maj \
  E3:maj7 E3:maj G3:maj B3:maj
```

---

### `generate_arpeggio_progression.py`

Generate arpeggiated chord progressions with finger patterns.

**Usage:**
```bash
./generate_arpeggio_progression.py [OPTIONS] CHORD [CHORD ...]
python scripts/generate_arpeggio_progression.py D2:m9 G2:9 C2:maj9 A2:m9
```

**Arguments:**
- `CHORDS`: Chord sequence as `Note:ChordType`

**Options:**
- `-o, --output`: Output MIDI file path (default: outputs/arpeggio_progression.mid)
- `--tempo`: Tempo in BPM (default: 550)
- `--volume`: MIDI volume 0-127 (default: 48)
- `--octaves`: Number of octaves to span (default: 4)
- `--pattern`: Finger pattern indices (default: [0, 2, 4, 5, 2, 4, 6, 8])

**Examples:**
```bash
# Generate arpeggios with default pattern
python scripts/generate_arpeggio_progression.py \
  D2:m9 G2:9 C2:maj9 A2:m9

# Custom finger pattern
python scripts/generate_arpeggio_progression.py \
  --pattern 0 1 2 3 4 5 \
  C4:maj G3:maj F3:maj
```

---

### `synthesize_guitar.py`

Synthesize realistic guitar strumming patterns with timing and dynamics.

**Usage:**
```bash
./synthesize_guitar.py [OPTIONS]
python scripts/synthesize_guitar.py --tempo 120 --loops 2
```

**Options:**
- `-o, --output`: Output MIDI file path (default: outputs/guitar_synthesis.mid)
- `--chord`: Guitar chord as comma-separated tabs (can use multiple times)
- `--duration`: Duration of each chord in beats (default: 4)
- `--pattern`: Strum pattern as space-separated values (default: 3 1 1 1 3 1 1 1 2 1 1)
- `--tempo`: Tempo in BPM (default: 70)
- `--volume`: Base MIDI volume 0-127 (default: 50)
- `--loops`: Number of repetitions (default: 4)
- `--drop-probability`: Probability of skipping strings (0-1, default: 0.0)
- `--strum-speed`: Strum speed multiplier (default: 1.0)
- `--note-duration`: Duration of each note in beats (default: 0.12)
- `--seed`: Random seed for reproducibility

**Examples:**
```bash
# Use default chord progression
python scripts/synthesize_guitar.py

# Custom chords and tempo
python scripts/synthesize_guitar.py \
  --chord "-1,0,2,2,1,0" \
  --chord "3,2,0,0,0,3" \
  --tempo 120 --loops 2

# With string dropping and faster strumming
python scripts/synthesize_guitar.py \
  --tempo 100 --drop-probability 0.2 --strum-speed 1.5
```

**Tab Format:**
Tabs are comma-separated fret positions:
- `-1` = String not played
- `0-12` = Fret position on that string

Example: `-1,0,2,2,1,0` (Em7 chord)

---

## Installation

All scripts require the pyMusic library to be installed:

```bash
# Install dependencies
pip install -r ../requirements.txt

# Make scripts executable (optional)
chmod +x *.py
```

## Running Scripts

### Method 1: Direct Execution
```bash
python scripts/generate_raga_melody.py --length 256
```

### Method 2: From Project Root
```bash
python scripts/generate_raga_melody.py --length 256
```

### Method 3: Using Python Path
```bash
cd scripts
python generate_raga_melody.py --length 256
```

## Output Files

By default, all scripts write to the `outputs/` directory:
- `outputs/raga_melody.mid`
- `outputs/chord_progression.mid`
- `outputs/arpeggio_progression.mid`
- `outputs/guitar_synthesis.mid`

Create the directory if it doesn't exist: `mkdir -p outputs`

## Supported Scales and Chords

### Scales
major, minor, harmonic_minor, dorian, phrygian, lydian, mixolydian, aeolian, locrian, major_pentatonic, minor_pentatonic, major_blues, minor_blues

### Chords
maj, m, dim, aug, sus2, sus4, 6, m6, 6/9, 7, maj7, m7, mMaj7, dim7, m7b5, 7b5, 7#5, 7b9, 7#9, maj7b5, maj7#5, m7#5, 7sus2, 7sus4, add9, 9, maj9, m9, mMaj9, sus9, 9sus4, m11, maj11, 11, m13, maj13, 13

## Tips

- Use `--seed` with `synthesize_guitar.py` for reproducible randomness
- Adjust `--volume` if MIDI sounds too quiet or loud
- Higher `--tempo` with lower `--duration` creates faster music
- Use `--drop-probability` with `synthesize_guitar.py` for humanized strumming
- Experiment with `--strum-speed` to create different playing styles

## Troubleshooting

If scripts fail to run:

1. Ensure you're in the project root directory
2. Check Python version (3.8+)
3. Install dependencies: `pip install -r requirements.txt`
4. Create outputs directory: `mkdir -p outputs`
5. Check file permissions: `chmod +x scripts/*.py`
