from panda3d.core import loadPrcFile # funct import to load configurations file
from direct.showbase.ShowBase import ShowBase

loadPrcFile("config/conf.prc")

class Game(ShowBase):
    def __init__(self):
        super(Game, self).__init__()

        box = self.loader.loadModel("models/box") # loads box.egg.pz, u dont even need to unzip the model lmao, very clever I must say
        box.setPos(0, 10, 0) # x is horizontal left-right, y is depth and z is vertical up-down, basically y is the z in threeJS and z is y in threeJS
        box.reparentTo(self.render) # makes the object appear in the scene

        panda = self.loader.loadModel("models/panda")
        panda.setPos(-2, 10, 0) # set position
        panda.setScale(0.2, 0.2, 0.2) # set scale
        panda.reparentTo(self.render)

game = Game()

# print(__builtins__.camera)

game.run()
