# Function Review

Scope: suggestion-only review. No code changes were made.
## Normalize calls to scales[scale_type] because those errors should say scale type not supported same for chord.
## `src/music_theory/core/notes.py`

- `build_diatonic_chord(note, scale_type, degree, num_notes)`: name `c_notes` more clearly and precompute the repeated
  scale steps; the current logic is correct but terse.
- `parse_chord_token(chord)`: factor the repeated `ValueError` text into one helper path; the root validation is good,
  but the validation branches can be flattened.
- `_build_chord_from_parts(...)`: split into smaller helpers for inversion handling, doubling, and openness selection;
  this is the biggest readability win in the file.
- `build_chord(...)`: already just a wrapper; fine as-is.
- `generate_chord_voicings(chord, octaves, filtered)`: extract the evenness key and filtering rule into named helpers,
  and avoid building `sorted([sorted(voicing) ...])` in one expression.
- `build_chord_from_pattern(chord, pattern)`: rename `pattern_indices` and `chord_pattern` to reflect the actual output;
  the `while` loop can be replaced with a clearer octave-normalization helper.
- `generate_all_chord_voicings(chord, octaves)`: already a thin wrapper; fine as-is.
- `are_same_pitch_classes(chord_1, chord_2)`: already concise; no meaningful shortening available.
- `have_same_inversion(chord_1, chord_2)`: same as above.
- `identify_chords_from_notes(notes_as_list)`: move `is_in_set` out of the function or inline it; also cache the
  pitch-class set once instead of recomputing it inside the inner loop.
- `calculate_mean_chord_distance(chord1, chord2, inversion, inversion2)`: already fine; could be a one-line return with
  no loss.
- `calculate_mean_chord_distance_between_notes(chord1, chord2)`: already compact; no change needed.
- `calculate_taxicab_distance_between_notes(chord1, chord2)`: replace `dist = 10000` with `float("inf")` and extract the
  alignment loop into a helper if you want it easier to read.
- `calculate_taxicab_distance(chord1, chord2, inversion, inversion2)`: already a direct wrapper.
- `find_closest_chord_inversion_by_mean(chord1, chord2, inversion)`: precompute `build_chord(chord2, inversion=inv)`
  once per candidate in a small loop to make the tuple construction less dense.
- `find_closest_chord_voicing_for_voice_leading(chord1, chord2, inversion)`: cache the base chord and the candidate list
  more explicitly; the current one-liner around `_build_chord_from_parts(...)` is hard to parse.
- `find_smooth_chord_voicing_from_notes(chord_one, chord_2)`: the logic is fine, but the candidate generation should be
  split out if you want it shorter and clearer.
- `find_chord_voicing_by_common_tones(chord1, chord2)`: this should be broken into helpers for matching common tones,
  scoring octave offsets, and selecting the best voicing; it is the least readable function in the file.

## `src/music_theory/core/chord.py`

- `ChordEvent.build_kwargs()`: fine as-is; could return the dict literal directly in a single expression, which is
  already what it does.
- `ScaledChordProgression.__init__(base_note)`: already minimal.
- `ScaledChordProgression.generate_progression(degrees, scale_type, chord_types)`: replace the nested index loops with
  `zip`/enumeration, name intermediate values more clearly, and split chord construction into a helper for readability.
- `build_arpeggio_from_chord(chord, length, pattern)`: remove the dead `# print(chord)` comment, avoid mutating
  `pattern` in-place, and compute the repeated pattern in a clearer helper.

## `src/music_theory/guitar/guitar_chord.py`

- `get_chord_from_tabs(tab)`: already concise.
- `max_muted_strings(n)`: fine as-is.
- `min_strings_played(n)`: fine as-is.
- `allow_open_strings(allow)`: return the lambda expression directly with a ternary to shorten it.
- `max_fret_span(span)`: factor the repeated `fretted` computation into a shared helper or inline the predicate if you
  want it shorter.
- `lowest_fret_at_least(fret)`: same recommendation as `max_fret_span`.
- `highest_fret_at_most(fret)`: same recommendation as `max_fret_span`.
- `bass_note_is(note)`: already small; could precompute and return a named predicate for clarity.
- `top_note_is(note)`: same as `bass_note_is`.
- `bass_note_in(notes)`: same as above, but the set precomputation is already the right optimization.
- `top_note_in(notes)`: same as above.
- `root_in_bass(root)`: just return `bass_note_is(root)` directly; this wrapper is unnecessary.
- `get_tabs_from_chord_notes(chord_notes, filters)`: split the recursive search into helpers for muting, fretting, and
  validation; the current function is correct but too dense to scan quickly.

## `src/music_theory/guitar/synthesizer.py`

- `GuitarChordPattern.__init__(tabs, chord_duration, pattern)`: consider `@dataclass` to remove boilerplate and make the
  class shorter.
- `GuitarChordPattern.__str__()`: fine as-is.
- `GuitarChordPattern.__repr__()`: can just alias `__str__` or be removed if not needed separately.
- `calculate_string_delay(string_index, total_strings, tempo, base_strum_speed)`: simplify the naming and inline the
  `normalized_position` variable if brevity matters.
- `calculate_note_time_in_pattern(...)`: too many parameters for a small calculation; group related timing inputs or
  precompute `chord_durations` externally.
- `calculate_velocity_for_string(...)`: `total_strings` is unused; remove it to make the signature smaller and clearer.
- `should_drop_string(string_index, drop_probability)`: `string_index` is unused; remove it to shorten the API.
- `synthesize_guitar_progression(...)`: hoist repeated values like `[cp.chord_duration for cp in chord_patterns]` out of
  the inner loop, and split note-generation, timing, and MIDI writing into helpers.

## `src/music_theory/midi/arpeggio.py`

- `_get_chord_intervals(chord_type)`: use `CHORD_DEFINITIONS.get(chord_type, default)` to shorten the branching.
- `generate_arpeggio_progression(...)`: compute `arpeggio_length`, the default finger pattern, and the chord conversion
  in smaller helpers; the current function is readable but could be flatter.

## `src/music_theory/midi/compose.py`

- `compose_chord_progression(...)`: this should be decomposed into helpers for section setup, pattern selection, and
  note writing; the nested loops make it harder to maintain than necessary.
- `_build_chord_event(chord_item)`: already concise; could be a one-line conditional expression if you want it shorter.

## `src/music_theory/raga/raga_generator.py`

- `generate_melody(raag, length)`: rename `raag` to `raga` consistently and remove the duplicated
  `get_note_at_index(...)` call by selecting the direction once.
- `generate_next_note(raag, current_note_index)`: the probability logic should be split into helper variables or a small
  decision table; the current branching is compact but not easy to reason about.
- `get_note_at_index(raag, index, scale_direction, base_note)`: already reasonably clear; the normalization math could
  be extracted if reused elsewhere.
- `parse_solfege(note_spec)`: replace the per-character loop with a small accidental-to-offset map and fold the
  `str(note_spec)` conversion into the start of the function.
- `melody_to_midi(melody, output_file, tempo, volume, beat_duration, return_midi)`: the write/return branches can be
  flattened, and `track`, `channel`, and `current_time` names can be made more explicit.
- `generate_raga_melody_prog(...)`: already a thin wrapper; fine as-is.

## `tests/chord_progression_test.py`

- `setUp()`: if it only sets constant fixture data, consider moving that data to class attributes or module-level
  constants.
- `test_init_default()`: already straightforward; no meaningful shortening.
- `test_init_custom_base()`: same as above.
- `test_gp_simple_degrees()`: if repeated patterns appear in other tests, parameterize them to reduce duplication.
- `test_gp_with_inversions()`: same as above.
- `test_gp_with_modal_interchange()`: same as above.
- `test_gp_custom_chord_types()`: same as above.
- `test_gp_does_not_mutate_chord_types()`: keep the current explicit assertions; clarity matters more than brevity here.
- `test_gp_different_scales()`: same as above.
- `test_basic_arpeggio()`: already compact.
- `test_arpeggio_with_pattern()`: already compact.
- `test_arpeggio_length()`: already compact.
- `test_arpeggio_repeating_pattern()`: already compact.
- `test_arpeggio_extended_range()`: already compact.
- `test_progression_to_arpeggio()`: if this is a broader integration check, keep it explicit rather than shorter.
- `test_get_note_on_arpeggiated_chord()`: already compact.

- `test_invalid_chord_tokens_raise_value_error()`: consider parameterizing the invalid cases to reduce repetition.


## `tests/test_raga_generator.py`

- `test_generate_next_note()`: if present, parameterize probability edge cases instead of duplicating setup.
- `test_melody_to_midi()`: keep explicit assertions; the test is likely doing enough already.

