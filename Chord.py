from Notes import get_scale_num


class ScaledChordProgression:

    def __init__(self, base_note=60):
        self.base_note = base_note

    def gp(self,degrees,scale_type = "major"):
        scale_notes = get_scale_num(self.base_note,scale_type)
        # print(scale_notes)
        for degree




