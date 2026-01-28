from Converter.sonicPiConverter import *

chords = [['D4', 'major_seventh', 2, [0],[0,1]],
          ['G4', 'dominant_seventh', 0, [0],[0,1]],
          # ['G4', 'dominant_seventh', 0, [0]],
          ['C4', 'major_seventh', 2,[0],[0,1]]]

for ch in chords :
    print(get_chord(*ch))

for ch in chords:
    print([x % 12 for x in get_chord(*ch ,over_octaves=1)])
    # [38, 42, 45, 49]
    # [43, 47, 50, 53]
    # [36, 40, 43, 47]

    # [2, 6, 9, 1]
    # [7, 11, 2, 5]
    # [0, 4, 7, 11]

for ch in chords:
    ch[0] = get_transpose_note(ch[0])

# print(generatePlayChordProg(chords,sleep=2))
print(generatePlayChordProgOnPattern([chords[0]],
                                     sleep_pattern=[x * 2 / 16 for x in [2,2,3]]))
print(generatePlayChordProgOnPattern([chords[1]],
                                     sleep_pattern=[x * 2 / 16 for x in [2,2,5]]))
print(generatePlayChordProgOnPattern([chords[2]],
                                     sleep_pattern=[x * 2 / 16 for x in [3,3,3,3,4]]))
for ch in chords:
    ch[0] = get_transpose_note(ch[0], 12 + 12)
# for chord in chords:
#     print(generatePlayArp(*chord , speed=0.5))

seq = get_chord(*chords[0])

seq.extend(get_chord(*chords[1]))
seq.extend(get_chord(*chords[2]))
seq.extend(get_chord(*chords[3]))

seq2 = sorted(s + 12 for s in seq)

seq3 = [get_num(x) + 12 for x in ['G4', 'A4', 'B4', 'D4', 'E4']] + [get_num(x) + 24 for x in
                                                                    ['G4', 'A4', 'B4', 'D4', 'E4']]

# print(generateRandSpeedVariation(seq3, len=128, subdivisions=[2, 4, 8]))
# print(generateRandSpeedVariation(seq3, len=32, subdivisions=[12]))
# print(playDrumBeat(":drum_snare_soft, amp: 2", [2/16 * x for x in [2,1,2,1,2,1,2,1,1,1,0.5,0.5,0.5,0.5]]))
# 2 2 2 2

# print(playDrumBeat(":sn_dolf, amp: 32", [2/16 * x for x in [3,3,2]]))
