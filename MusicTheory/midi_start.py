import random

from midiutil import MIDIFile

from MusicTheory.Chord import ScaledChordProgression, arpeggiate_chord

track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 550   # In BPM
volume   = 30  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)
scp = ScaledChordProgression(40)  # C3 as base
cp = scp.gp([(2,1),(-2,3),(1,2),(1,1)], "major" , [[1, 3, 5, 7,9],[1, 3, 5, 7,9],[1, 3, 5, 7,9],[1, 3, 5, 7,9]])

reps = 4
cp1 = []
# for chord in cp:
#     for _ in range(reps):
#         cp1 += [chord]
# print(cp1)
# for i,chord in enumerate(cp1):
#     for j,note in enumerate(chord):
#         MyMIDI.addNote(track, channel, note, time + i + j * 0.02, duration  - 0.1, volume if i%4==0 else int(volume//1.3))
#

pattern_length = 32
block = [1,3,2,1]
pattern = []
while len(pattern) <= pattern_length:
    pattern.extend(block)
    block = [x+1 for x in block]

pattern.extend(block)
pattern = pattern[:pattern_length]
print(pattern)
print(len(pattern))



arp = [arpeggiate_chord(ch,pattern_length,pattern) for ch in cp]



for i,ch in enumerate(arp):
    print((ch))
    print(len(ch))
    for j,note in enumerate(ch):
        MyMIDI.addNote(track, channel, note, time + i*pattern_length + j , duration,volume)


#
# for i,ch in enumerate(arp):
#     # print((ch))
#     # print(len(ch))
#     for j,note in enumerate(ch):
#         if random.random() > 0.5:
#             MyMIDI.addNote(track, channel, note - 12, time + i*pattern_length + j + duration/2 , duration,volume)
#




with open("../Temp/major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)