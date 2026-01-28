from MusicTheory.Chord import ScaledChordProgression, arpeggiate_chord
from MusicTheory.Notes import get_note

scp = ScaledChordProgression(48)
chord_types = [[0,2,4,6] for _ in range(4)]
chord_types[1] = [2,4,6,8]
chord_types[2] = [0,2,4]
chord_types[3] = [0,2,4]
cp = scp.gp([(2), (4,1), (6), (3)], "major",chord_types)
for ch in cp:
    print(ch)
    # print([(get_note(x)) for x in ch])



for ch in cp:
    arp = arpeggiate_chord(ch, 16, [0,1,3,2,0,1,2,3])
    print(" ".join([str(get_note(x)) for x in arp]))
