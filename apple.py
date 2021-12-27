from panda3d.core import NodePath


class Apple():
    def __init__(self, loader, color):  # color should be a Vec4
        self.apple: NodePath = loader.loadModel("objects/apple.stl")
        # print("apple is " +  str(type(self.apple)))
        # print("color in apple is " + str(color))
        self.apple.setColor(color)
        self.apple.setScale(0.02, 0.02, 0.02)
        self.is_intruder = False

    def get_apple(self):
        return self.apple
