import unittest
from typing import List, Tuple, Union
from Notes import *


class TestMusicTheory(unittest.TestCase):

    def test_get_num(self):
        self.assertEqual(get_num("C5"), 60)
        self.assertEqual(get_num("As0"), 10)
        self.assertEqual(get_num("Fs5"), 66)
        self.assertEqual(get_num("D4"), 50)
        self.assertEqual(get_num("B3"), 47)
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
        self.assertEqual(get_chord(30, 'major' , lo_double_notes=[0]), [18,30, 34, 37])
        self.assertEqual(get_chord(36, 'minor',2), [43,48,51])
        self.assertEqual(get_chord(55, 'dominant_seventh', 3), [65, 67, 71, 74])
        self.assertEqual(get_chord(50, 'augmented'), [50, 54, 58])
        self.assertEqual(get_chord(53, 'diminished'), [53, 56, 59])
        self.assertEqual(get_chord(52, 'sus4',1,uo_double_notes=[2]), [57, 59, 64, 71])
        self.assertEqual(get_chord(57, 'major_seventh'), [57, 61, 64, 68])
        self.assertEqual(get_chord(59, 'minor_seventh'), [59, 62, 66, 69])
        self.assertEqual(get_chord(48, 'major_ninth', 2), [55, 59, 60, 62, 64])
        self.assertEqual(get_chord(74, 'dominant_thirteenth'), [74, 78, 81, 84, 88, 97])
        self.assertEqual(get_chord(74, 'dominant_thirteenth', 3), [84, 86, 88, 90, 93, 97])
        self.assertEqual(get_chord(77, 'sus9'), [77, 79, 84, 91])
        self.assertEqual(get_chord(79, '6/9'), [79, 81, 83, 86, 88, 93])

    def test_transpose_note(self):
        self.assertEqual(get_transpose_note('C5'), 'C6')
        self.assertEqual(get_transpose_note('C5', -1), 'C4')
        self.assertEqual(get_transpose_note('C5', 2), 'C7')
        self.assertEqual(get_transpose_note(60), 'C6')

    def test_transpose_note(self):
        self.assertEqual(get_transpose_num('C5'), 72)
        self.assertEqual(get_transpose_num('C5', -1), 48)
        self.assertEqual(get_transpose_num('C5', 2), 84)
        self.assertEqual(get_transpose_num(60), 72)

    def test_get_mean_chord_distance(self):
        result = get_mean_chord_distance(60, "major", 67, "minor")
        self.assertAlmostEqual(result, 6.66, delta=0.1)  # Replace with the expected result
        result = get_mean_chord_distance(72, "major", 76, "minor", inversion=1, inversion2=2)
        self.assertAlmostEqual(result, 7.66 ,  delta=0.1)  # Replace with the expected result

    def test_get_mean_chord_distance_chord(self):
        result = get_mean_chord_distance_chord([60, 64, 67], [67, 70, 74])
        self.assertAlmostEqual(result, 6.66, delta=0.1)  # Replace with the expected result
        result = get_mean_chord_distance_chord([60, 64], [67, 70, 74])
        self.assertAlmostEqual(result, 8.33, delta=0.1)  # Replace with the expected result

    def test_get_closest_inversion(self):
        result = get_closest_inversion(60, "major", 67, "minor", 1)
        self.assertEqual(result, [67, 70, 74])  # Replace with the expected result
        result = get_closest_inversion(72, "minor", 76, "major", 2)
        print(get_note(72))
        print(get_note(76))
        print(get_chord(72, "minor",2), sum(get_chord(72, "minor",2))/3)
        print(get_chord(76, "major" ,0), sum(get_chord(76, "major" ,0))/3)
        print(get_chord(76, "major" ,1), sum(get_chord(76, "major" ,1))/3)
        print(get_chord(76, "major" ,2), sum(get_chord(76, "major" ,2))/3)
        self.assertEqual(result, [80, 83, 88])  # Replace with the expected result


if __name__ == '__main__':
    unittest.main()
