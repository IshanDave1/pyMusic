from src.music_theory.raga.raga_generator import generate_melody, melody_to_midi, raag

# Generate a melody of 16 notes
melody = generate_melody(raag, 32*4)

print("Generated melody (midi_note, duration):")
for i, (note, duration) in enumerate(melody):
    print(f"  {i}: note={note}, duration={duration}")

# Write to MIDI file
output_path = "./outputs/test_raga_2.mid"
melody_to_midi(melody, output_path, tempo=480, volume=80)
print(f"\nMIDI file written to {output_path}")
