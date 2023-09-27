from sonicPiConverter import *

chords = [['D4', 'major_ninth', 0, [0]],
          ['A3', 'minor', 2, [0]],
          ['E4', 'minor_major_seventh', 0, [0]],
          ['G4', 'major_sixth', 0, [0]]]

# print(generatePlayChordProg(chords,sleep=2))
# print(generatePlayChordProgOnPattern(chords,
#                                      sleep_pattern=[x * 2 / 16 for x in [3,3,4,2,4]]))

chords = [['D5', 'major_ninth', 0],
          ['A4', 'minor', 2],
          ['E5', 'minor_major_seventh', 0],
          ['G5', 'major_sixth', 0]]
# for chord in chords:
#     print(generatePlayArp(*chord , speed=0.5))

seq = get_chord(*chords[0])

seq.extend(get_chord(*chords[1]))
# seq.extend(get_chord(*chords[2]))
seq.extend(get_chord(*chords[3]))

seq2 = sorted(s + 12 for s in seq)

#print(generateRandSpeedVariation(seq + seq2[:4],len = 128,subdivisions=[2,4,8]))
# print(generateRandSpeedVariation(seq2[:6],len = 32,subdivisions=[12]))
# print(playDrumBeat(":drum_snare_soft, amp: 2", [2/16 * x for x in [2,1,2,1,2,1,2,1,1,1,0.5,0.5,0.5,0.5]]))
# print(playDrumBeat(":sn_dolf, amp: 32", [2/16 * x for x in [3,3,2]]))