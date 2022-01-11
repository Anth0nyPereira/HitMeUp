from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.bullet import BulletWorld
from panda3d.core import loadPrcFile, Point3, Vec2, CollisionTraverser, \
    CollisionHandlerQueue, CollisionNode, BitMask32, CollisionRay, NodePath, \
    Shader, DirectionalLight, ShadeModelAttrib, PointLight, Material, \
    AmbientLight  # funct import to load configurations file
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec4, Vec3
from axis_helper import AxisHelper
from apple import Apple
from color import Color
import random
from math import pi, sin, cos

loadPrcFile("config/conf.prc")

available_apples = []
timestamps = []


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        # self.box = self.loader.loadModel("models/box")  # loads box.egg.pz, u dont even need to unzip the model lmao, very clever I must say
        # self.box.setPos(0, 50, 0)  # x is horizontal left-right, y is depth and z is vertical up-down, basically y is the z in threeJS and z is y in threeJS
        # self.box.reparentTo(self.render)  # makes the object appear in the scene

        self.create_apples()

        # dict that stores keys to control the game itself
        self.keyMap = {"up": False, "down": False, "left": False, "right": False, "shoot": False, "w": False,
                       "s": False, "a": False, "d": False, }

        # tell panda3d to handle the events -- tell directobject class to accept the events, a pair for each key,
        # when it's pressed and when it's released
        self.accept("w", self.update_key_map, ["up", True])
        self.accept("s", self.update_key_map, ["down", True])
        self.accept("a", self.update_key_map, ["left", True])
        self.accept("d", self.update_key_map, ["right", True])

        self.accept("arrow_up", self.update_key_map, ["up", True])
        self.accept("arrow_down", self.update_key_map, ["down", True])
        self.accept("arrow_left", self.update_key_map, ["left", True])
        self.accept("arrow_right", self.update_key_map, ["right", True])

        self.accept("mouse3", self.update_key_map, ["shoot", True])

        self.accept("w-up", self.update_key_map, ["up", False])
        self.accept("s-up", self.update_key_map, ["down", False])
        self.accept("a-up", self.update_key_map, ["left", False])
        self.accept("d-up", self.update_key_map, ["right", False])

        self.accept("arrow_up-up", self.update_key_map, ["up", False])
        self.accept("arrow_down-up", self.update_key_map, ["down", False])
        self.accept("arrow_left-up", self.update_key_map, ["left", False])
        self.accept("arrow_right-up", self.update_key_map, ["right", False])

        self.accept("mouse3-up", self.update_key_map, ["shoot", False])

        self.accept("mouse1", self.mouse_click)
        self.accept('wheel_up', self.zoom_in)
        self.accept('wheel_down', self.zoom_out)

        self.updateTask = self.taskMgr.add(self.update, "update")

        self.axis_helper = AxisHelper(10).get_axis()
        self.axis_helper.reparentTo(self.render)

        self.update_counter = 0

        self.last_mouse_position = Vec2(0, 0)

        self.camera.setPos(0, -10, 0)

        # ser collisionTraverser  and collision handler
        self.picker = CollisionTraverser()
        # self.picker.showCollisions(self.render)
        self.pq = CollisionHandlerQueue()

        self.pickerNode = CollisionNode("mouse_raycast")
        self.pickerNP = self.camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(BitMask32.bit(1))
        # self.box.setCollideMask(BitMask32.bit(1))

        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(self.pickerNP, self.pq)

        self.taskMgr.add(self.camera_control, "Camera Control")

        # lighting and shading experiment
        '''
        plight = PointLight('plight')
        plight.setColor((0.4, 0.4, 0.0, 0.3))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(20, -20, 0)
        self.render.setLight(plnp)
        
        '''
        self.alight = AmbientLight('alight')
        self.alight.setColor((0.2, 0.2, 0.2, 1))
        self.alight_nodepath = self.render.attachNewNode(self.alight)
        self.render.setLight(self.alight_nodepath)


    def zoom_in(self):
        self.camera.set_y(self.camera, 5)

    def zoom_out(self):
        self.camera.set_y(self.camera, -5)

    def camera_control(self, task):
        dt = globalClock.getDt()
        if dt > 0.20:
            return task.cont

        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            self.camera.setP(mpos.getY() * 30)
            self.camera.setH(mpos.getX() * -50)
            if 0.1 > mpos.getX() > -0.1:
                self.camera.setH(self.camera.getH())
            else:
                self.camera.setH(self.camera.getH() + mpos.getX() * -1)

        if self.keyMap["up"]:
            self.camera.setPos(self.camera.getPos() + Vec3(0, 15.0 * dt, 0))
        if self.keyMap["down"]:
            self.camera.setPos(self.camera.getPos() + Vec3(0, -15.0 * dt, 0))
        if self.keyMap["left"]:
            self.camera.setPos(self.camera.getPos() + Vec3(-10.0 * dt, 0, 0))
        if self.keyMap["right"]:
            self.camera.setPos(self.camera.getPos() + Vec3(10.0 * dt, 0, 0))

        return task.cont

    # this method will be called when the event of pressing one of the available keys will occur
    def update_key_map(self, key, value):
        self.keyMap[key] = value
        # print(controlName, "set to", controlState)

    def create_apples(self):
        # get 2 random colors
        tuple_colors = Color.generate_2_random_colors()

        # create 3 identical apples
        for i in range(3):
            apple = Apple(self.loader, tuple_colors[0].value).get_apple()
            apple.setCollideMask(BitMask32.bit(1))
            apple.setName("other")
            available_apples.append(apple)

        # the ugly duck :(
        apple = Apple(self.loader, tuple_colors[1].value).get_apple()
        apple.setCollideMask(BitMask32.bit(1))
        apple.setName("outlandish")
        available_apples.append(apple)

        # positioning all apples
        random.shuffle(available_apples)
        pos = 0
        for apple in available_apples:
            apple.setPos(pos, 0, 0)
            apple.reparentTo(self.render)
            pos += 1

    def mouse_click(self):

        # check if we have access to the mouse
        if self.mouseWatcherNode.hasMouse():

            # get the mouse position
            mpos = self.mouseWatcherNode.getMouse()

            # set the position of the ray based on the mouse position
            self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())
            self.picker.traverse(self.render)
            # if we have hit something sort the hits so that the closest is first and highlight the node
            if self.pq.getNumEntries() > 0:
                self.pq.sortEntries()

                pickedObj: NodePath = self.pq.getEntry(0).getIntoNodePath()
                parent_picked_obj = pickedObj.parent.parent  # while debugging, discovered that needed to check the great-grandfather node

                if parent_picked_obj in available_apples and parent_picked_obj.getName() == "outlandish":
                    print("You got it right!")
                    pickedObj.detachNode()
                    pickedObj.removeNode()
                else:
                    print("Wrong, try again!")

    def shoot(self):
        print("shooting")
        mousePos = self.mouseWatcherNode.getMouse()
        mousePos3d = (mousePos[0], 0, mousePos[1])
        print(mousePos3d)

        # mousePosButton = button.getRelativePoint(self.render, mousePos3d)

    def add_shader2(self):
        print("entering add_shader2")
        # available_apples[0].node().setAttrib(ShadeModelAttrib.make(ShadeModelAttrib.MFlat)) # this doesnt work, go next
        # available_apples[1].node().setAttrib(ShadeModelAttrib.make(ShadeModelAttrib.MSmooth))

    def add_shader(self):
        available_apples[0]: NodePath
        available_apples[0].setShaderInput("lightColor", self.alight.getColor())
        available_apples[0].setShaderInput("lightPosition", self.alight_nodepath.getPos())
        available_apples[0].setShaderInput("viewerPosition", (self.camera.getPos()))
        '''
        available_apples[0].setShaderInput("material.ambient", (0.6, 0.6, 0, 1.0))
        available_apples[0].setShaderInput("material.specular", (1.0, 1.0, 1.0, 1.0))
        available_apples[0].setShaderInput("material.diffuse", (1.0, 1.0, 0, 1.0))
        available_apples[0].setShaderInput("material.shininess", 32.0)
        '''

        # available_apples[0].setShaderInput("model", available_apples[0].node().) TODO: how to calculate model,
        #  view and projection matrixes

        shader = Shader.load(Shader.SL_GLSL,
                             vertex="shaders/vertex_shader_Illumination_pervertex.glsl",
                             fragment="shaders/fragment_shader_illumination_pervertex.glsl")
        available_apples[0].setShader(shader)

        # available_apples[0].node().setAttrib(ShadeModelAttrib.make(ShadeModelAttrib.MFlat))

    # update loop
    def update(self, task):
        # self.add_shader()
        # self.add_shader2()

        # Get the amount of time since the last update
        dt = globalClock.getDt()
        # print(dt)
        timestamps.append(dt)
        if self.update_counter % 5000 == 0:
            for i in range(len(available_apples)):
                available_apples[i].detachNode()
                available_apples[i].removeNode()
            available_apples.clear()
            # timestamps.clear()
            self.create_apples()


        if self.keyMap["shoot"]:
            self.shoot()

        self.update_counter += 1
        return task.cont  # task.cont exists to make this task run forever


game = Game()

# print(__builtins__.camera)

game.run()
