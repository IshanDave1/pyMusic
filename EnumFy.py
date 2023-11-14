from enum import Enum


class Note(Enum):
    C = 0
    Cs = 1
    D = 2
    Ds = 3
    E = 4
    F = 5
    Fs = 6
    G = 7
    Gs = 8
    A = 9
    As = 10
    B = 11
# ... Add more notes here


# Loop through all enum values
for note in Note:
    print(f"Note: {note}")
