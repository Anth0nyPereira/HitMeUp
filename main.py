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
        # panda.reparentTo(box) # box is parented to the renderer, thats why panda still appears in the scene

        self.keyMap = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "shoot": False
        }

        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("mouse1", self.updateKeyMap, ["shoot", True])
        self.accept("mouse1-up", self.updateKeyMap, ["shoot", False])

        

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        print(controlName, "set to", controlState)

game = Game()

# print(__builtins__.camera)

game.run()
