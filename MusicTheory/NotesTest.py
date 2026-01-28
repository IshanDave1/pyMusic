import unittest

from Notes import *


class TestMusicTheory(unittest.TestCase):

    def test_get_num(self):
        self.assertEqual(get_num("C"), 60)  # default octave is 5
        self.assertEqual(get_num("c"), 60)  # default octave is 5
        self.assertEqual(get_num("C5"), 60)
        self.assertEqual(get_num("c5"), 60)
        self.assertEqual(get_num("As0"), 10)
        with self.assertRaises(ValueError):
            get_num("k")
        with self.assertRaises(ValueError):
            get_num("Es3")

    def test_get_note(self):
        self.assertEqual(get_note(72), "C6")
        self.assertEqual(get_note(30), "Fs2")
        self.assertEqual(get_note(66), "Fs5")
        self.assertEqual(get_note(50), "D4")
        self.assertEqual(get_note(47), "B3")

    def test_get_scale_num(self):
        self.assertEqual(get_scale_num(72, 'major'), [72, 74, 76, 77, 79, 81, 83])
        self.assertEqual(get_scale_num('C6', 'major'), [72, 74, 76, 77, 79, 81, 83])
        self.assertEqual(get_scale_num('As0', 'dorian'), [10, 12, 13, 15, 17, 19, 20])
        self.assertEqual(get_scale_num(66, 'lydian'), [66, 68, 70, 72, 73, 75, 77])

    def test_get_scale_notes(self):
        self.assertEqual(get_scale_notes(72, 'major'), ["C6", "D6", "E6", "F6", "G6", "A6", "B6"])
        self.assertEqual(get_scale_notes('C6', 'major'), ["C6", "D6", "E6", "F6", "G6", "A6", "B6"])
        self.assertEqual(get_scale_notes('As0', 'dorian'), ['As0', 'C1', 'Cs1', 'Ds1', 'F1', 'G1', 'Gs1'])
        self.assertEqual(get_scale_notes(66, 'lydian'), ['Fs5', 'Gs5', 'As5', 'C6', 'Cs6', 'Ds6', 'F6'])
        with self.assertRaises(ValueError):
            get_scale_notes(72, 'invalid_scale')  # Invalid scale, should raise ValueError

    def test_get_chord(self):
        # major 0,4,7
        with self.assertRaises(ValueError):
            get_chord('Z0', 'major')
        with self.assertRaises(ValueError):
            get_chord('Z0', 'major')
        self.assertEqual(get_chord(30, 'major'), [30, 34, 37])  # major chord
        self.assertEqual(get_chord(30, 'major', inversion=1), [34, 37, 30 + 12])  # major chord 1st inversion
        self.assertEqual(get_chord(30, 'major', inversion=2), [37, 30 + 12, 34 + 12])  # major chord 2nd inversion
        self.assertEqual(get_chord(30, 'major', lo_double_notes=[0]),
                         [30 - 12, 30, 34, 37])  # major chord with the root note in lower octave
        self.assertEqual(get_chord(30, 'major', uo_double_notes=[2]),
                         [30, 34, 37, 37 + 12])  # major chord with the root note in lower octave

        # minor 7th -> 4 notes 0,3,7,10 :
        self.assertEqual(get_chord(30, 'minor_seventh'), [30, 33, 37, 40])  # minor_seventh chord
        self.assertEqual(get_chord(30, 'minor_seventh', inversion=1),
                         [33, 37, 40, 30 + 12])  # minor_seventh chord 1st inversion
        self.assertEqual(get_chord(30, 'minor_seventh', inversion=2),
                         [37, 40, 30 + 12, 33 + 12])  # minor_seventh chord 2nd inversion
        self.assertEqual(get_chord(30, 'minor_seventh', inversion=3),
                         [40, 30 + 12, 33 + 12, 37 + 12])  # minor_seventh chord 3rd inversion
        self.assertEqual(get_chord(30, 'minor_seventh', lo_double_notes=[0]),
                         [30 - 12, 30, 33, 37, 40])  # minor_seventh chord with the root note in lower octave
        self.assertEqual(get_chord(30, 'minor_seventh', uo_double_notes=[2]),
                         [30, 33, 37, 40, 37 + 12])  # minor_seventh chord with the root note in lower octave

        self.assertEqual(get_chord(74, 'dominant_thirteenth'), [74, 78, 81, 84, 88, 97])
        self.assertEqual(get_chord(74, 'dominant_thirteenth', 3, over_octaves=2),
                         sorted([84, 88, 97, 74 + 12, 78 + 12, 81 + 12]))  # all chords must be sorted

        self.assertEqual(get_chord(30, 'major', inversion=2), [37, 30 + 12, 34 + 12])  # major chord 2nd inversion
        self.assertEqual(get_chord(30, 'major', inversion=2, over_octaves=1),
                         [37, 30 + 12, 34 + 12])  # major chord 2nd inversion
        self.assertEqual(get_chord(36, 'minor', 2, over_octaves=2), [43, 60, 63])
        self.assertEqual(get_chord(36, 'minor', over_octaves=3), [36, 39, 67])
        self.assertEqual(get_chord(36, 'minor', over_octaves=3, openness=0.599), [36, 63, 67])
        self.assertEqual(get_chord(36, 'minor', over_octaves=3, openness=0.999), [36, 51, 67])

    def test_transpose_note(self):
        self.assertEqual(get_transpose_note('C5'), 'C6')
        self.assertEqual(get_transpose_note('C5', -1), 'C4')
        self.assertEqual(get_transpose_note('C5', 2), 'C7')
        self.assertEqual(get_transpose_note(60), 'C6')

    def test_transpose_note(self):
        self.assertEqual(get_transpose_num('C5'), 72)
        self.assertEqual(get_transpose_num('C5', -12), 48)
        self.assertEqual(get_transpose_num('C5', 24), 84)
        self.assertEqual(get_transpose_num(60), 72)

    def test_get_mean_chord_distance(self):
        result = get_mean_chord_distance(60, "major", 67, "minor")
        self.assertAlmostEqual(result, 6.66, delta=0.1)
        result = get_mean_chord_distance(72, "major", 76, "minor", inversion=1, inversion2=2)
        self.assertAlmostEqual(result, 7.66, delta=0.1)

    def test_get_mean_chord_distance_chord(self):
        result = get_mean_chord_distance_chord([60, 64, 67], [67, 70, 74])
        self.assertAlmostEqual(result, 6.66, delta=0.1)
        result = get_mean_chord_distance_chord([60, 64], [67, 70, 74])
        self.assertAlmostEqual(result, 8.33, delta=0.1)

    def test_get_closest_inversion(self):
        result = get_closest_inversion(60, "major", 67, "minor", 1)
        self.assertEqual(result, [67, 70, 74])
        result = get_closest_inversion(72, "minor", 76, "major", 2)
        self.assertEqual(result, [80, 83, 88])

    def test_get_inversion(self):
        result = get_inversion([0, 4, 7], 1)
        expected = [[0, 4, 7]]
        self.assertEqual(result, expected)
        result = get_inversion([0, 4, 7], 2)
        expected = [[0, 16, 19], [4, 12, 19], [0, 4, 19], [0, 7, 16]]
        self.assertEqual(result, expected)
        result = get_inversion([0, 4, 7], 3)
        expected = [[0, 28, 31], [0, 4, 31], [4, 24, 31], [0, 7, 28], [4, 12, 31], [0, 19, 28], [0, 16, 31]]
        self.assertEqual(result, expected)

    def test_get_inversion_unfiltered(self):
        result = get_inversion_unfiltered([0, 4, 7], 1)
        expected = [[0, 4, 7]]
        self.assertEqual(result, expected)
        result = get_inversion_unfiltered([0, 4, 7], 2)
        expected = [[0, 4, 7], [12, 16, 19], [4, 7, 12], [7, 12, 16], [0, 16, 19], [4, 12, 19], [0, 4, 19], [0, 7, 16]]
        self.assertEqual(result, expected)
        result = get_inversion_unfiltered([0, 4, 7], 3)
        expected = [[0, 4, 7], [12, 16, 19], [24, 28, 31], [4, 7, 12], [16, 19, 24], [7, 12, 16], [19, 24, 28],
                    [0, 16, 19], [12, 28, 31], [4, 7, 24], [4, 12, 19], [16, 24, 31], [0, 4, 19], [12, 16, 31],
                    [0, 7, 16], [12, 19, 28], [7, 24, 28], [7, 16, 24], [4, 19, 24], [7, 12, 28], [0, 28, 31],
                    [0, 4, 31], [4, 24, 31], [0, 7, 28], [4, 12, 31], [0, 19, 28], [0, 16, 31]]

        self.assertEqual(result, expected)

    def test_is_same_chord(self):
        self.assertTrue(is_same_chord([60, 64, 67], [60, 67, 64]))  # Same notes, different order
        self.assertTrue(is_same_chord([60, 64, 67], [60, 67, 64, 72]))  # Same notes, different order and octave
        self.assertFalse(is_same_chord([60, 64, 67], [60, 64, 68]))  # Different notes
        self.assertTrue(
            is_same_chord([60, 64, 67], [60, 64, 67, 72]))  # Different number of notes with only octave variations

    def test_is_same_inversion(self):
        self.assertTrue(is_same_inversion([60, 64, 67], [60 + 12, 64 - 12, 67]))  # Same notes, different octaves
        self.assertFalse(is_same_inversion([60, 64, 67], [64, 67, 60]))  # Same notes, different order

    def test_get_taxicab_chord_distance_chord(self):
        self.assertEqual(16, get_taxicab_chord_distance_chord([60, 64, 67], [60 + 12, 64 - 12, 67]))  #
        self.assertEqual(0, get_taxicab_chord_distance_chord([2, 3, 4], [1, 2, 3, 4, 5]))  #

    def test_get_taxicab_chord_distance(self):
        self.assertEqual(0, get_taxicab_chord_distance(60, "major", 60, "major"))  #
        self.assertEqual(12, get_taxicab_chord_distance(60, "major", 60, "major", inversion2=1))  #


if __name__ == '__main__':
    unittest.main()
