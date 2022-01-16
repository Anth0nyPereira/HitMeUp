from panda3d.core import TextNode


class Text:
    def __init__(self, name, input_str, color):
        self.name = name
        self.input_str = input_str

        self.text = TextNode(name)
        self.text.setText(input_str)
        self.text.setTextColor(color)

        self.text.setShadow(0.05, 0.05)
        self.text.setShadowColor(0, 0, 0, 0.5)

    def get_text(self):
        return self.text

    def set_text(self, txt):
        self.text.clearText()
        self.text.setText(txt)
