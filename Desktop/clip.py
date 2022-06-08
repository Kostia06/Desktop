import clipboard as cp

class Clip_Board():
    def __init__(self):
        self.clip_list = []
        self.new = False

    def update(self):
        if cp.paste() != None and cp.paste() != '':
            if not cp.paste() in self.clip_list:
                if len(self.clip_list) <= 9:
                    self.new = False
                    self.clip_list.append(cp.paste())
                else:
                    self.new = True
                    self.clip_list.pop(0)
                    self.clip_list.append(cp.paste())
    def copy(self, text):
        cp.copy(str(text))

