import unittest

from src.music_theory.core.chord import ChordEvent
from src.music_theory.core.notes import (
    build_chord,
    calculate_mean_chord_distance,
    note_string_to_midi,
    parse_chord_token,
)


class TestChordTokens(unittest.TestCase):
    def test_omitted_quality_defaults_to_major_at_middle_octave(self):
        self.assertEqual(build_chord("E"), build_chord("E4:maj"))

    def test_quality_is_colon_delimited(self):
        self.assertEqual(parse_chord_token("D2:m9"), ("D2", "m9"))
        self.assertEqual(parse_chord_token("C:6/9"), ("C", "6/9"))

    def test_sharps_and_flats_are_supported(self):
        self.assertEqual(note_string_to_midi("Cs4"), note_string_to_midi("C#4"))
        self.assertEqual(note_string_to_midi("Db4"), note_string_to_midi("Cs4"))
        self.assertEqual(note_string_to_midi("Cb4"), note_string_to_midi("B3"))
        self.assertEqual(build_chord("Bb:m7"), build_chord("As:m7"))

    def test_invalid_chord_tokens_raise_value_error(self):
        for token in ("", "E:", ":m9", "E:maj:7", "E:unknown", "Efoo"):
            with self.assertRaises(ValueError):
                parse_chord_token(token)

    def test_chord_event_controls_voicing(self):
        event = ChordEvent("C:maj", inversion=1)
        self.assertEqual(event.build_kwargs()["inversion"], 1)

    def test_chord_spec_distance_api(self):
        self.assertAlmostEqual(calculate_mean_chord_distance("C", "G"), 7.0)

if __name__ == "__main__":
    unittest.main()
