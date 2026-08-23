# DRY Review

Scope: identify function pairs or groups that repeat the same logic and could be reconciled.

## `src/music_theory/guitar/guitar_chord.py`

- `max_fret_span(span)`, `lowest_fret_at_least(fret)`, `highest_fret_at_most(fret)`: all build the same `fretted` list and then apply one bound check. Extract a shared helper that returns the fretted notes once, then parameterize the check.
- `bass_note_is(note)` and `top_note_is(note)`: both compute a pitch class and compare it against either the first or last sounding note. A generic position-based predicate would remove the duplication.
- `bass_note_in(notes)` and `top_note_in(notes)`: same shape as above, but comparing against a set. This should be the same generic helper as `bass_note_is` / `top_note_is`.

## `src/music_theory/core/notes.py`

- `calculate_mean_chord_distance(chord1, chord2, inversion, inversion2)` and `calculate_taxicab_distance(chord1, chord2, inversion, inversion2)`: both are wrappers around the note-list distance functions. If API clarity is not needed, they could be folded into a shared chord-pair distance helper.
- `calculate_mean_chord_distance_between_notes(chord1, chord2)` and `calculate_taxicab_distance_between_notes(chord1, chord2)`: both search over chord alignments and compare candidate distances. They differ only in scoring, so the alignment loop should be shared.
- `note_to_midi(note)` and `transpose_to_midi(note, semitones)`: both normalize a note input to MIDI and then apply a simple transformation. Not identical, but they sit on the same conversion path and should keep parsing centralized.

## `src/music_theory/midi/compose.py`

- `_build_chord_event(chord_item)` is the single normalization point for chord inputs. Keep it as the shared dispatch layer so `compose_chord_progression(...)` does not need its own branching for `ChordEvent` vs string inputs.

## `src/music_theory/guitar/synthesizer.py`

- `calculate_string_delay(...)`, `calculate_velocity_for_string(...)`, and `should_drop_string(...)` are small, separate helpers that are already acting like shared primitives. Avoid inlining them into `synthesize_guitar_progression(...)`; if anything, they could be grouped into a small timing/dynamics helper module.
- `GuitarChordPattern.__str__()` and `GuitarChordPattern.__repr__()` currently render the same data. `__repr__` can just alias `__str__` or be removed if no separate representation is needed.

## `src/music_theory/raga/raga_generator.py`

- `generate_melody(raag, length)` and `generate_next_note(raag, current_note_index)` both encode direction-dependent branching. The specific work is different, but the ascent/descent decision should be centralized so the same rule is not re-derived in multiple places.

## Highest-value merges

1. Merge `max_fret_span`, `lowest_fret_at_least`, and `highest_fret_at_most` behind one helper.
2. Merge `bass_note_is` / `top_note_is` and `bass_note_in` / `top_note_in` behind one generic position-based predicate.
3. Share the chord-alignment search used by `calculate_mean_chord_distance_between_notes` and `calculate_taxicab_distance_between_notes`.
