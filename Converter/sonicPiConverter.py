import random
import time

import numpy as np

from MusicTheory.Notes import *


def generatePlayNote(note):
    return f'play {note if str(note).isdigit() else get_num(note)}'


def generatePlayChord(base_note, chord_type, inversion=0, lo_double_notes=None, uo_double_notes=None, octaves=1,
                      openness=0.0):
    return '\n'.join(
        [f'play {note}' for note in
         get_chord(base_note, chord_type, inversion, lo_double_notes, uo_double_notes, over_octaves=octaves,
                   openness=openness)])


def generatePlayChordProg(chords, sleep=1, octaves=1, openness=0.0):
    return f'\nsleep {sleep}\n'.join(
        [generatePlayChord(x[0], x[1], x[2], over_octaves=octaves, openness=openness) for x in
         chords]) + f'\nsleep {sleep}'


def generatePlayChordProgOnPattern(chords, sleep_pattern, octaves=1, openness=0.0):
    s = ""
    for ch in chords:
        for pt in sleep_pattern:
            s = s + generatePlayChord(ch[0], ch[1], ch[2], ch[3], ch[4], octaves=octaves,
                                      openness=openness) + f"\nsleep {pt}\n"

    return s


def generatePlayArp(base_note, chord_type, inversion=0, speed=1.0):
    chord = np.array(get_chord(base_note, chord_type, inversion))
    np.random.shuffle(chord)

    return '\n'.join([f'play {note}\nsleep {speed}' for note in chord][:4])


def generateRand(seq, speed=1.0, len=8):
    return '\n'.join(f'{generatePlayNote(random.choice(seq))}\nsleep {speed}' for _ in range(len))


def generateRandSpeedVariation(seq, speed=1.0, len=8, subdivisions=None):
    seed_value = int(time.time())
    random.seed(seed_value)
    if subdivisions is None:
        subdivisions = [1]
    return '\n'.join(
        f'{generatePlayNote(random.choice(seq))}\nsleep {speed / (random.choice(subdivisions))}' for _ in range(len))


def playDrumBeat(sample, subdivisions):
    s = ""
    for pt in subdivisions:
        s = f"{s}sample {sample}" + f"\nsleep {pt}\n"

    return s


def generatePlayArpChord(chord, speed=1.0):
    np.random.shuffle(chord)

    return '\n'.join([f'play {note}\nsleep {speed}' for note in chord][:4])


def generatePlayChordChord(chord):
    return '\n'.join(
        [f'play {note}' for note in chord])

def generatePlayChordChordPattern(chord,pattern,speed):
    chs = '\n'.join(
        [f'play {note}' for note in chord])

    s = ''
    for pt in pattern :
        s +=chs
        s+= f'\nsleep {pt/speed}\n'
    return s


prog = [[50, 53, 57, 60, 64, 67], [48, 52, 57, 59, 62, 67], [48, 52, 57, 59, 65, 67], [50, 52, 59, 60, 65, 67]]
pattern = [[3, 3, 3, 3, 4],[3, 3, 3, 3, 2, 2], [3, 3, 3, 3, 2, 2], [3, 3, 3, 3, 1, 1, 2]]
for i in range(4):
    for j in range(len(prog)):
        print(generatePlayChordChordPattern(prog[j], pattern[j], speed=4))
