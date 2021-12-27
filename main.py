from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import loadPrcFile # funct import to load configurations file
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec4, Vec3
from axis_helper import AxisHelper

loadPrcFile("config/conf.prc")

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.box = self.loader.loadModel("models/box") # loads box.egg.pz, u dont even need to unzip the model lmao, very clever I must say
        self.box.setPos(0, 10, 0) # x is horizontal left-right, y is depth and z is vertical up-down, basically y is the z in threeJS and z is y in threeJS
        self.box.reparentTo(self.render) # makes the object appear in the scene

        panda = self.loader.loadModel("models/panda")
        panda.setPos(-2, 10, 0) # set position
        panda.setScale(0.2, 0.2, 0.2) # set scale
        panda.reparentTo(self.render)
        # panda.reparentTo(box) # box is parented to the renderer, thats why panda still appears in the scene

        apple = self.loader.loadModel("objects/apple.stl")
        apple.reparentTo(self.render)

        # dict that stores keys to control the game itself
        self.keyMap = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "shoot": False
        }

        # tell panda3d to handle the events -- tell directobject class to accept the events, a pair foreach key, when it's pressed and when it's released
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

        self.updateTask = self.taskMgr.add(self.update, "update")

        self.axis_helper = AxisHelper(10).get_axis()
        self.axis_helper.reparentTo(self.render)

    # this method will be called when the event of pressing one of the available keys will occur
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        print(controlName, "set to", controlState)

    # update loop
    def update(self, task):
        # Get the amount of time since the last update
        dt = globalClock.getDt()

        # If any movement keys are pressed, use the above time
        # to calculate how far to move the character, and apply that.
        if self.keyMap["up"]:
            self.box.setPos(self.box.getPos() + Vec3(0, 5.0 * dt, 0))
        if self.keyMap["down"]:
            self.box.setPos(self.box.getPos() + Vec3(0, -5.0 * dt, 0))
        if self.keyMap["left"]:
            self.box.setPos(self.box.getPos() + Vec3(-5.0 * dt, 0, 0))
        if self.keyMap["right"]:
            self.box.setPos(self.box.getPos() + Vec3(5.0 * dt, 0, 0))
        if self.keyMap["shoot"]:
            print("Zap!")

        return task.cont # task.cont exists to make this task run forever

game = Game()

# print(__builtins__.camera)

game.run()
