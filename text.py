from direct.gui.OnscreenText import OnscreenText


class Text:
    def __init__(self, input_str, pos_x, pos_y, scale):
        self.input_str = input_str
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.scale = scale
        self.textObject = OnscreenText(text=self.input_str, pos=(self.pos_x, self.pos_y), scale=self.scale)

    def get_text(self):
        return self.textObject

    def set_text(self, txt):
        self.textObject = OnscreenText(text=txt, pos=(self.pos_x, self.pos_y), scale=self.scale)
