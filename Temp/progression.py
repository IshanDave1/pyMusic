from MusicTheory.Notes import *

scale = 'major'
base_note = 'C4'
n = 6


def generate_progression(base_note, scale, chords):
    return [get_scale_chord(base_note, scale, chords[i][0], chords[i][1]) for i in range(len(chords))]


def generate_smooth_progression(base_note, scale, chords):
    progression = generate_progression(base_note, scale, chords)
    smooth_progression = list()
    smooth_progression.append(progression[0])
    for i in range(1, len(chords)):
        prev = smooth_progression[i - 1]
        next = get_closest_taxicab_inversion_chord(prev, progression[i])
        smooth_progression.append(next)

    return smooth_progression


print(get_num('C4'))
print(get_scale_degree('C4', 'major', 2))
print(get_scale_chord('C4', 'major', 5, 4))
progression = generate_progression(base_note, scale, [[2, n], [5, n], [1, n]])
# print(progression)  # mdM


smooth_progression = generate_smooth_progression(base_note, scale, [[2, n], [6, n],[4, n], [1, n]])
print(smooth_progression)  # mdM
#
# assert is_same_chord(progression[0], get_chord('D4', 'minor_seventh'))
# assert is_same_chord(progression[1], get_chord('G4', 'dominant_seventh'))
# assert is_same_chord(progression[2], get_chord('C4', 'major_seventh'))
#
#
# assert is_same_chord(smooth_progression[0], get_chord('D4', 'minor_seventh'))
# assert is_same_chord(smooth_progression[1], get_chord('G4', 'dominant_seventh'))
# assert is_same_chord(smooth_progression[2], get_chord('C4', 'major_seventh'))

# print(get_closest_taxicab_inversion('D4', 'minor_seventh', 'G4', 'major_seventh', 0))
