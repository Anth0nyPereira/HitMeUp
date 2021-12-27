from direct.showbase.ShowBase import ShowBase


class Apple():
    def __init__(self, loader, color):  # color should be a Vec4
        self.apple = loader.loadModel("objects/apple.stl")
        self.apple.setColor(color)
        self.apple.setScale(0.02, 0.02, 0.02)

    def get_apple(self):
        return self.apple
