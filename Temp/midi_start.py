from midiutil import MIDIFile

degrees  = [60, 62, 64, 65, 67, 69, 71]
degrees = degrees + [x + 12 for x in degrees] + [x + 24 for x in degrees] # MIDI note number
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 60   # In BPM
volume   = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)



for i in range(len(degrees)-5):
    MyMIDI.addNote(track, channel, degrees[i], time + i, duration, volume)
    MyMIDI.addNote(track, channel, degrees[i+2], time + i, duration, volume)
    MyMIDI.addNote(track, channel, degrees[i+4], time + i, duration, volume)

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)