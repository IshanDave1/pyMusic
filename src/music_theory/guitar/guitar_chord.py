from src.music_theory.core.notes import note_string_to_midi

STANDARD_GUITAR_TUNING_NOTES = ["E2", "A2", "D3", "G3", "B3", "E4"]
STANDARD_GUITAR_TUNING_MIDI = [note_string_to_midi(note) for note in STANDARD_GUITAR_TUNING_NOTES]

NUM_STRINGS = 6
MAX_FRET = 14
MAX_STRETCH = 4
MUTED = -1


def get_chord_from_tabs(tab):
    """
    Convert a guitar tab into sounding MIDI notes.
    Returned in pitch order (lowest -> highest).
    """
    return sorted(
        STANDARD_GUITAR_TUNING_MIDI[string] + fret
        for string, fret in enumerate(tab)
        if fret != MUTED
    )


# ----------------------------------------------------------------------
# Geometry Filters
# ----------------------------------------------------------------------

def max_muted_strings(n):
    return lambda tab: tab.count(MUTED) <= n


def min_strings_played(n):
    return lambda tab: sum(f != MUTED for f in tab) >= n


def allow_open_strings(allow=True):
    if allow:
        return lambda tab: True
    return lambda tab: all(f != 0 for f in tab if f != MUTED)


def max_fret_span(span):
    def filt(tab):
        fretted = [f for f in tab if f > 0]
        return not fretted or max(fretted) - min(fretted) <= span
    return filt


def lowest_fret_at_least(fret):
    def filt(tab):
        fretted = [f for f in tab if f > 0]
        return not fretted or min(fretted) >= fret
    return filt


def highest_fret_at_most(fret):
    def filt(tab):
        fretted = [f for f in tab if f > 0]
        return not fretted or max(fretted) <= fret
    return filt


# ----------------------------------------------------------------------
# Pitch Filters
# ----------------------------------------------------------------------

def bass_note_is(note):
    pitch_class = note_string_to_midi(note) % 12
    return lambda tab: get_chord_from_tabs(tab)[0] % 12 == pitch_class


def top_note_is(note):
    pitch_class = note_string_to_midi(note) % 12
    return lambda tab: get_chord_from_tabs(tab)[-1] % 12 == pitch_class


def bass_note_in(notes):
    pitch_classes = {
        note_string_to_midi(note) % 12
        for note in notes
    }

    return lambda tab: (
        get_chord_from_tabs(tab)[0] % 12 in pitch_classes
    )


def top_note_in(notes):
    pitch_classes = {
        note_string_to_midi(note) % 12
        for note in notes
    }

    return lambda tab: (
        get_chord_from_tabs(tab)[-1] % 12 in pitch_classes
    )


def root_in_bass(root):
    return bass_note_is(root)


# ----------------------------------------------------------------------
# Generator
# ----------------------------------------------------------------------

def get_tabs_from_chord_notes(chord_notes, filters=()):
    chord_pitch_classes = {
        note_string_to_midi(note) % 12
        for note in chord_notes
    }

    tabs = []

    def search(tab):
        current_string = len(tab)

        if current_string == NUM_STRINGS:
            played_pitch_classes = {
                (STANDARD_GUITAR_TUNING_MIDI[string] + fret) % 12
                for string, fret in enumerate(tab)
                if fret != MUTED
            }

            if (
                played_pitch_classes == chord_pitch_classes
                and all(f(tab) for f in filters)
            ):
                tabs.append(tab[:])

            return

        previous_fret = float("inf") if current_string == 0 else tab[-1]

        previous_pitch_class = (
            None
            if current_string == 0 or tab[-1] == MUTED
            else (
                STANDARD_GUITAR_TUNING_MIDI[current_string - 1]
                + tab[-1]
            ) % 12
        )

        # mute string
        tab.append(MUTED)
        search(tab)
        tab.pop()

        open_string = STANDARD_GUITAR_TUNING_MIDI[current_string]

        for pitch_class in chord_pitch_classes:

            if pitch_class == previous_pitch_class:
                continue

            first_fret = (pitch_class - open_string) % 12

            for fret in (first_fret, first_fret + 12):

                if fret > MAX_FRET:
                    continue

                if (
                    current_string == 0
                    or tab[-1] == MUTED
                    or abs(previous_fret - fret) <= MAX_STRETCH
                ):
                    tab.append(fret)
                    search(tab)
                    tab.pop()

    search([])
    tabs.sort()
    return tabs


# ----------------------------------------------------------------------
# Examples
# ----------------------------------------------------------------------

if __name__ == "__main__":

    print("\nExample 1 - All C major voicings")
    print(get_tabs_from_chord_notes(
        ["C2", "E2", "G2"]
    ))

    print("\nExample 2 - Root in bass")
    print(get_tabs_from_chord_notes(
        ["C2", "E2", "G2"],
        filters=[
            root_in_bass("C2")
        ]
    ))

    print("\nExample 3 - No open strings")
    print(get_tabs_from_chord_notes(
        ["C2", "E2", "G2"],
        filters=[
            allow_open_strings(False)
        ]
    ))

    print("\nExample 4 - Compact jazz voicings")
    print(get_tabs_from_chord_notes(
        ["F2", "A2", "C2","E2"],
        filters=[
            max_fret_span(3),
            min_strings_played(4),
            max_muted_strings(2),
            lowest_fret_at_least(3),
            highest_fret_at_most(8)
        ]
    ))

    print("\nExample 5 - Melody on G")
    print(get_tabs_from_chord_notes(
        ["E","Gs","B"],
        filters=[max_muted_strings(0)]
    ))