from random import randint

from src.music_theory.core.chord import ScaledChordProgression
from src.music_theory.core.notes import build_chord, extend_notes_across_octaves, midi_to_note_string

chord_names = [
    "A3:m",
    "C4:m",
    "F3:M",
    "F3:M",
]
chords = []

scp = ScaledChordProgression(52)
c2 = scp.generate_progression([2,7,4,1],'minor',[[1,3,5,7]]*4)
# chords = [[54, 57, 60, 64], [62, 66, 69, 72], [57, 60, 64, 67], [52, 55, 59, 62]]
print("c2",c2)

for i in range(len(c2)):
    chord = extend_notes_across_octaves(c2[i], 6)
    chords.append(chord)

print(chords)

length_of_arpeggio = 32
phrase_length = 8
min_total_jump = 2
max_total_jump = 3
next_arpeggio_jump = -1


def gen_delta(phrase_length, max_jump=3):
    delta = []
    for i in range(1, phrase_length):
        jump = randint(-max_jump, max_jump)
        while jump == 0 or jump + sum(delta) < 0:
            jump = randint(-max_jump, max_jump)
        delta.append(jump)
    return delta


while True:
    delta = gen_delta(phrase_length)
    if delta[0] > 0 and min_total_jump <= sum(delta) <= max_total_jump:
        break

print(delta)
start_index = 0
indices = []
while len(indices) < length_of_arpeggio:
    indices.append(start_index)
    for i in range(len(delta)):
        start_index += delta[i]
        indices.append(start_index)
    start_index += next_arpeggio_jump

print(indices)

for chord in chords:
    a_ = ' '.join([midi_to_note_string(chord[idx]) for idx in indices])

    print(f'[{a_}]')
