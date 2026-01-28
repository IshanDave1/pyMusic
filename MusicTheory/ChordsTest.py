"""
Unit tests for the Chord module.

Tests the ScaledChordProgression class and arpeggiate_chord function.
"""

import unittest
from MusicTheory.Chord import ScaledChordProgression, arpeggiate_chord
from MusicTheory.Notes import get_note


class TestScaledChordProgression(unittest.TestCase):
    """Tests for the ScaledChordProgression class."""

    def setUp(self):
        """Set up test fixtures."""
        self.scp = ScaledChordProgression(48)  # C3 as base note
        self.scp_middle_c = ScaledChordProgression(60)  # C5 as base note

    def test_init_default(self):
        """Test default initialization with middle C."""
        scp = ScaledChordProgression()
        self.assertEqual(scp.base_note, 60)

    def test_init_custom_base(self):
        """Test initialization with custom base note."""
        scp = ScaledChordProgression(48)
        self.assertEqual(scp.base_note, 48)

    def test_gp_simple_degrees(self):
        """Test chord progression with simple integer degrees."""
        # I-IV-V-I progression in C major starting at C3 (48)
        cp = self.scp.gp([1, 4, 5, 1], "major")
        
        # Verify we get 4 chords
        self.assertEqual(len(cp), 4)
        
        # Each chord should be a triad (3 notes) by default
        for chord in cp:
            self.assertEqual(len(chord), 3)
        
        # First chord should be C major triad: C3, E3, G3 = 48, 52, 55
        self.assertEqual(cp[0], [48, 52, 55])
        
        # Fourth chord (F major): F3, A3, C4 = 53, 57, 60
        self.assertEqual(cp[1], [53, 57, 60])
        
        # Fifth chord (G major): G3, B3, D4 = 55, 59, 62
        self.assertEqual(cp[2], [55, 59, 62])

    def test_gp_with_inversions(self):
        """Test chord progression with inversions (tuple of 2)."""
        # (4, 1) means IV chord in first inversion
        cp = self.scp.gp([(1, 0), (4, 1)], "major")
        
        self.assertEqual(len(cp), 2)
        
        # First chord: C major root position
        self.assertEqual(cp[0], [48, 52, 55])
        
        # Second chord: F major first inversion (A in bass)
        # F major = F, A, C -> first inversion starts from A
        # Should be A3, C4, F4 = 57, 60, 65
        self.assertEqual(cp[1], [57, 60, 65])

    def test_gp_with_modal_interchange(self):
        """Test chord progression with modal interchange (tuple of 3)."""
        # (4, 0, "minor") borrows iv from parallel minor
        cp = self.scp.gp([1, (4, 0, "minor")], "major")
        
        self.assertEqual(len(cp), 2)
        
        # First chord: C major
        self.assertEqual(cp[0], [48, 52, 55])
        
        # Second chord: F minor (borrowed from C minor)
        # F minor = F, Ab, C = 53, 56, 60
        self.assertEqual(cp[1], [53, 56, 60])

    def test_gp_custom_chord_types(self):
        """Test chord progression with custom chord voicings."""
        # Use 7th chords: [1, 3, 5, 7]
        chord_types = [[1, 3, 5, 7], [1, 3, 5, 7]]
        cp = self.scp.gp([1, 5], "major", chord_types)
        
        # Each chord should have 4 notes
        for chord in cp:
            self.assertEqual(len(chord), 4)
        
        # C major 7: C, E, G, B = 48, 52, 55, 59
        self.assertEqual(cp[0], [48, 52, 55, 59])

    def test_gp_does_not_mutate_chord_types(self):
        """Test that gp() doesn't mutate the input chord_types list."""
        chord_types = [[1, 3, 5], [1, 3, 5]]
        original = [ct.copy() for ct in chord_types]
        
        self.scp.gp([1, 2], "major", chord_types)
        
        # chord_types should be unchanged
        self.assertEqual(chord_types, original)

    def test_gp_different_scales(self):
        """Test chord progression with different scale types."""
        # Minor scale
        cp_minor = self.scp.gp([1], "minor")
        # C minor triad: C, Eb, G = 48, 51, 55
        self.assertEqual(cp_minor[0], [48, 51, 55])
        
        # Dorian scale
        cp_dorian = self.scp.gp([1], "dorian")
        # C dorian i chord: C, Eb, G = 48, 51, 55 (same as minor for triad)
        self.assertEqual(cp_dorian[0], [48, 51, 55])


class TestArpeggiateChord(unittest.TestCase):
    """Tests for the arpeggiate_chord function."""

    def test_basic_arpeggio(self):
        """Test basic arpeggiation without pattern."""
        chord = [60, 64, 67]  # C major triad
        arp = arpeggiate_chord(chord, 6)
        
        self.assertEqual(len(arp), 6)
        # Extended chord is [60, 64, 67, 72, 76, 79, 84, 88, 91]
        # Default pattern is [0, 1, 2, 3, 4, 5, 6, 7, 8]
        # First 6 notes: 60, 64, 67, 72, 76, 79
        self.assertEqual(arp, [60, 64, 67, 72, 76, 79])

    def test_arpeggio_with_pattern(self):
        """Test arpeggiation with custom pattern."""
        chord = [60, 64, 67]  # C major triad
        pattern = [0, 1, 2, 1]  # Up and back
        arp = arpeggiate_chord(chord, 4, pattern)
        
        self.assertEqual(len(arp), 4)
        # Pattern [0, 1, 2, 1] on extended chord
        # Index 0 = 60, 1 = 64, 2 = 67
        self.assertEqual(arp, [60, 64, 67, 64])

    def test_arpeggio_length(self):
        """Test that arpeggio respects length parameter."""
        chord = [60, 64, 67]
        
        for length in [4, 8, 16]:
            arp = arpeggiate_chord(chord, length)
            self.assertEqual(len(arp), length)

    def test_arpeggio_repeating_pattern(self):
        """Test arpeggiation with pattern that repeats."""
        chord = [60, 64, 67]
        pattern = [0, 2]  # Alternates root and fifth
        arp = arpeggiate_chord(chord, 6, pattern)
        
        self.assertEqual(len(arp), 6)
        # Pattern repeats: 0, 2, 0, 2, 0, 2
        self.assertEqual(arp, [60, 67, 60, 67, 60, 67])

    def test_arpeggio_extended_range(self):
        """Test that arpeggiation extends chord across octaves."""
        chord = [60, 64, 67]
        # Access notes in higher octaves
        pattern = [0, 3, 6]  # Root in 3 different octaves
        arp = arpeggiate_chord(chord, 3, pattern)
        
        # Index 0 = 60 (C4), 3 = 72 (C5), 6 = 84 (C6)
        self.assertEqual(arp, [60, 72, 84])

    def test_arpeggio_assertion_on_invalid_pattern(self):
        """Test that invalid pattern indices raise AssertionError."""
        chord = [60, 64, 67]  # 3 notes, extended to 9
        pattern = [0, 1, 10]  # Index 10 is out of range
        
        with self.assertRaises(AssertionError):
            arpeggiate_chord(chord, 3, pattern)


class TestIntegration(unittest.TestCase):
    """Integration tests combining ScaledChordProgression and arpeggiate_chord."""

    def test_progression_to_arpeggio(self):
        """Test creating a progression and arpeggiating each chord."""
        scp = ScaledChordProgression(60)
        cp = scp.gp([1, 4, 5], "major")
        
        pattern = [0, 1, 2, 1]
        
        for chord in cp:
            arp = arpeggiate_chord(chord, 8, pattern)
            self.assertEqual(len(arp), 8)
            # First note should be root of chord
            self.assertEqual(arp[0], chord[0])

    def test_get_note_on_arpeggiated_chord(self):
        """Test that arpeggiated notes convert to valid note names."""
        chord = [60, 64, 67]  # C major
        arp = arpeggiate_chord(chord, 4, [0, 1, 2, 1])
        
        note_names = [get_note(n) for n in arp]
        self.assertEqual(note_names, ['C5', 'E5', 'G5', 'E5'])


if __name__ == '__main__':
    unittest.main()
