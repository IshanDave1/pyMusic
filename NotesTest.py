import unittest
from typing import List, Tuple, Union
from Notes import *


class TestMusicTheory(unittest.TestCase):

    def test_get_num(self):
        self.assertEqual(get_num("C6"), 72)
        self.assertEqual(get_num("As0"), 10)
        self.assertEqual(get_num("Fs5"), 66)
        self.assertEqual(get_num("D4"), 50)
        self.assertEqual(get_num("B3"), 47)

    def test_get_note(self):
        self.assertEqual(get_note(72), "C6")
        self.assertEqual(get_note(10), "As0")
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

    def test_get_chord(self):
        # We need to implement the get_chord function first
        pass


if __name__ == '__main__':
    unittest.main()
