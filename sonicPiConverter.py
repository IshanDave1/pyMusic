from Notes import *
import random
import numpy as np


def generatePlayNote(note):
    return f'play {note if str(note).isdigit else get_num(note)}'


def generatePlayChord(base_note, chord_type, inversion=0):
    return '\n'.join([f'play {note}' for note in get_chord(base_note, chord_type, inversion)])


def generatePlayChordProg(chords, sleep=1):
    return f'\nsleep {sleep}\n'.join([generatePlayChord(x[0], x[1], x[2]) for x in chords]) + f'\nsleep {sleep}'


def generatePlayChordProgOnPattern(chords, sleep_pattern):
    s = ""
    for ch in chords:
        for pt in sleep_pattern:
            s = s + generatePlayChord(ch[0], ch[1], ch[2]) + f"\nsleep {pt}\n"

    return s


def generatePlayArp(base_note, chord_type, inversion=0, speed=1.0):
    chord = np.array(get_chord(base_note, chord_type, inversion))
    np.random.shuffle(chord)

    return '\n'.join([f'play {note}\nsleep {speed}' for note in chord][:4])


def generateRand(seq, speed=1.0, len=8):
    return '\n'.join(f'{generatePlayNote(random.choice(seq))}\nsleep {speed}' for _ in range(len))


def generateRandSpeedVariation(seq, speed=1.0, len=8, subdivisions=None):
    if subdivisions is None:
        subdivisions = [1]
    return '\n'.join(
        f'{generatePlayNote(random.choice(seq))}\nsleep {speed / (random.choice(subdivisions))}' for _ in range(len))

#
# print(generatePlayChord('C5' , 'major_seventh'))
# print('sleep 2')
# print(generatePlayChord('C5' , 'major_seventh'))
# print('sleep 2')
# print(generatePlayChord('D5' , 'dominant_seventh'))
# print('sleep 2')
# print(generatePlayChord('G5' , 'dominant_seventh'))
# print('sleep 2')

# print(generatePlayArp('C6' , 'major_seventh',speed = 0.5))
# print(generatePlayArp('C6' , 'major_seventh',speed = 0.5))
# print(generatePlayArp('D6' , 'dominant_seventh',speed = 0.5))
# print(generatePlayArp('G6' , 'dominant_seventh',speed = 0.5))

# print(generatePlayChord('A4' , 'minor_seventh'))
# print('sleep 2')
# print(generatePlayChord('G4' , 'minor_seventh'))
# print('sleep 2')
#
# scale = get_scale_num('D6', 'minor')
# scale2 = get_scale_num('D7', 'minor')
#
# print(generateRandSpeedVariation(scale, speed=0.5, len=8 * 4))
# print(generateRandSpeedVariation(scale, speed=0.5, len=6,subdivisions=[3]))
# print(generateRandSpeedVariation(scale, speed=0.5, len=8 * 2,subdivisions=[1,2]))
# print(generateRandSpeedVariation(scale + scale2, speed=0.5, len=6,subdivisions=[3]))
# print(generateRandSpeedVariation(scale, speed=0.5, len=8 * 2,subdivisions=[1,2,4]))
# print(generateRandSpeedVariation(scale2, speed=0.5, len=12,subdivisions=[6]))


# Cmaj9 (C - E - G - B - D)
# F#m13 (F# - A# - C# - E - G# - B - D#)
# Bm9 (B - D# - F# - A - C#)
# E13 (E - G# - B - D# - F# - A)
# Amaj9 (A - C# - E - G# - B)


# 3
# print(generatePlayArp('A4' , 'minor_seventh',speed = 0.5))
# print(generatePlayArp('G4' , 'minor_seventh',speed = 0.5))
# scale = get_scale_num('F6', 'minor')
# scale2 = get_scale_num('F7', 'minor')
#
# print(generateRandSpeedVariation(scale, speed=0.5, len=8 * 4))
# print(generateRandSpeedVariation(scale, speed=0.5, len=6,subdivisions=[3]))
# print(generateRandSpeedVariation(scale, speed=0.5, len=8 * 2,subdivisions=[1,2]))
# print(generateRandSpeedVariation(scale + scale2, speed=0.5, len=6,subdivisions=[3]))
# print(generateRandSpeedVariation(scale, speed=0.5, len=8 * 2,subdivisions=[1,2,4]))
# print(generateRandSpeedVariation(scale2, speed=0.5, len=12,subdivisions=[6]))


# 4
# print(generatePlayChord('Ds4' , 'major_seventh_flat_five'))
# print('sleep 2')
# print(generatePlayChord('C4' , 'major_seventh'))
# print('sleep 2')
# print(generatePlayChord('G4' , 'dominant_seventh'))
# print('sleep 2')
# print(generatePlayChord('D4' , 'minor_seventh'))
# print('sleep 2')

# print(generatePlayArp('Ds4' , 'major_seventh_flat_five',speed = 0.5))
# print(generatePlayArp('C4' , 'major_seventh',speed = 0.5))
# print(generatePlayArp('G4' , 'dominant_seventh',speed = 0.5))
# print(generatePlayArp('D4' , 'minor_seventh',speed = 0.5))

# # 5
# print(generatePlayChord('D6', 'major_ninth'))
# print('sleep 2')
# print(generatePlayChord('A6', 'minor_eleventh'))
# print('sleep 2')
# print(generatePlayChord('E6', 'minor_seventh_sharp_five'))
# print('sleep 2')
# print(generatePlayChord('G6', 'major_sixth'))
# print('sleep 2')


# print(generatePlayArp('D6', 'major_ninth', speed=0.25))
# print(generatePlayArp('D6', 'major_ninth', speed=0.25))
#
# print(generatePlayArp('A5', 'minor_eleventh',2, speed=0.25))
# print(generatePlayArp('A5', 'minor_eleventh',2, speed=0.25))
#
# print(generatePlayArp('E5', 'minor_seventh_sharp_five',2, speed=0.25))
# print(generatePlayArp('E5', 'minor_seventh_sharp_five',2, speed=0.25))
#
# print(generatePlayArp('G6', 'major_sixth', speed=0.25))
# print(generatePlayArp('G6', 'major_sixth', speed=0.25))
