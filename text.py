from panda3d.core import TextNode


class Text:
    def __init__(self, render, name, input_str, scale, color):
        self.name = name
        self.input_str = input_str
        self.scale = scale
        self.render = render

        self.text = TextNode(name)
        self.text.setText(input_str)
        self.text.setTextColor(color)

        self.text.setShadow(0.05, 0.05)
        self.text.setShadowColor(1, 0, 0, 0.5)

        self.textObject = self.render.attachNewNode(self.text)
        self.textObject.setScale(scale)

    def get_text(self):
        return self.textObject

    def set_text(self, txt):
        self.text.setText(txt)
