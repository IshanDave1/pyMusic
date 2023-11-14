import matplotlib.pyplot as plt
import numpy as np

import Notes


def draw_chord(chord_notes):
    note_labels = {
        21: 'An0', 22: 'Bbn0', 23: 'Bn0', 24: 'Cn1', 25: 'C#1', 26: 'Dn1', 27: 'Ebn1', 28: 'En1', 29: 'Fn1', 30: 'F#1',
        31: 'Gn1', 32: 'G#1', 33: 'An1', 34: 'Bbn1', 35: 'Bn1', 36: 'Cn2', 37: 'C#2', 38: 'Dn2', 39: 'Ebn2', 40: 'En2',
        41: 'Fn2',
        42: 'F#2', 43: 'Gn2', 44: 'G#2', 45: 'An2', 46: 'Bbn2', 47: 'Bn2', 48: 'Cn3', 49: 'C#3', 50: 'Dn3', 51: 'Ebn3',
        52: 'En3', 53: 'Fn3', 54: 'F#3', 55: 'Gn3', 56: 'G#3', 57: 'An3', 58: 'Bbn3', 59: 'Bn3', 60: 'Cn4', 61: 'C#4',
        62: 'Dn4', 63: 'Ebn4', 64: 'En4', 65: 'Fn4', 66: 'F#4', 67: 'Gn4', 68: 'G#4', 69: 'An4', 70: 'Bbn4', 71: 'Bn4',
        72: 'Cn5', 73: 'C#5', 74: 'Dn5', 75: 'Ebn5', 76: 'En5', 77: 'Fn5', 78: 'F#5', 79: 'Gn5', 80: 'G#5', 81: 'An5',
        82: 'Bbn5', 83: 'Bn5', 84: 'Cn6', 85: 'C#6', 86: 'Dn6', 87: 'Ebn6', 88: 'En6', 89: 'Fn6', 90: 'F#6', 91: 'Gn6',
        92: 'G#6', 93: 'An6', 94: 'Bbn6', 95: 'Bn6', 96: 'Cn7', 97: 'C#7', 98: 'Dn7', 99: 'Ebn7', 100: 'En7', 101: 'Fn7',
        102: 'F#7', 103: 'Gn7', 104: 'G#7', 105: 'An7', 106: 'Bbn7', 107: 'Bn7', 108: 'Cn8'
    }
    for val in note_labels.values():
        if len(val) == 2:
            val = f"{val} "

    # Create a figure and axis for plotting
    fig, ax = plt.subplots(figsize=(12, 3))

    # Define the range of MIDI notes for the keyboard
    min_note = chord_notes[0] - 5  # Minimum MIDI note
    max_note = chord_notes[-1] + 5 # Maximum MIDI note

    # Create an array of zeros to represent the piano keys
    keys = np.zeros(max_note - min_note + 1)

    # Color the keys corresponding to the chord
    for note in chord_notes:
        keys[note - min_note] = 3  # Lighter color

    # Plot the piano keys
    ax.imshow([keys], cmap='Greys', aspect='auto', extent=[min_note, max_note, 0, 1])

    # Label the keys with their note names
    for note, label in note_labels.items():
        if min_note <= note <= max_note:
            ax.text(note, 0.5, label, ha='center', va='center', fontsize=10, color='red')

    # Set the plot limits
    ax.set_xlim(min_note - 1, max_note + 1)
    ax.set_ylim(0, 1)

    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])

    # Show the plot
    plt.show()


# Example usage
chord = Notes.get_chord(40 , 'diminished_seventh') # Cn6, En6, Gn6
draw_chord(chord)
