import copy

from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.bullet import BulletWorld
from panda3d.core import loadPrcFile, Point3, Vec2, CollisionTraverser, \
    CollisionHandlerQueue, CollisionNode, BitMask32, CollisionRay, NodePath, \
    Shader, DirectionalLight, ShadeModelAttrib, PointLight, Material, \
    AmbientLight, CardMaker, CollisionSphere, LPoint3f  # funct import to load configurations file
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec4, Vec3
from panda3d.physics import ForceNode, LinearVectorForce, PhysicsCollisionHandler, ActorNode

from axis_helper import AxisHelper
from apple import Apple
from color import Color
import random

from plane import Plane

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

        # self.accept("mouse3", self.update_key_map, ["shoot", True])

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

        self.camera.setPos(0, -10, 0.5)

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
        # available_apples[0].node().parent.parent.setLight(self.alnp2)
        '''
        self.alight = AmbientLight('alight')
        self.alight.setColor((0.2, 0.2, 0.2, 1))
        self.alight_nodepath = self.render.attachNewNode(self.alight)
        self.render.setLight(self.alight_nodepath)
        '''

        self.card_maker = None
        self.create_card_maker()

        self.create_floor()

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
            apple_object = Apple(self.loader, tuple_colors[0].value, self.render)
            apple = apple_object.get_apple()
            apple.setCollideMask(BitMask32.bit(1))
            apple.setName("other")
            apple_object.set_light_to_apple()
            available_apples.append(apple)

        # the ugly duck :(
        apple_object = Apple(self.loader, tuple_colors[1].value, self.render, True)
        apple = apple_object.get_apple()
        # apple_object.set_light_to_apple()
        apple_object.set_texture_to_apple()
        # print(type(apple)) # nodepath

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



    def add_shader2(self):
        print("entering add_shader2")
        # available_apples[0].node().setAttrib(ShadeModelAttrib.make(ShadeModelAttrib.MFlat)) # this doesnt work, go next
        # available_apples[1].node().setAttrib(ShadeModelAttrib.make(ShadeModelAttrib.MSmooth))

    def create_card_maker(self):
        # create the plane

        cm = CardMaker("plane")
        # set the size of the card (left, right, bottom, top - in XZ-plane)
        cm.setFrame(-2, 2, -2, 2)
        self.plane = self.render.attachNewNode(cm.generate())
        # the card is created vertically in the XZ-plane, so it has to be rotated
        # to make it horizontal
        # self.plane.setP(-90.)
        self.plane.setPos(0, -5, 10)

        road_tex = self.loader.loadTexture("textures/sample.jpg")
        self.plane.setTexture(road_tex)

        # collision
        # enable physics
        self.enableParticles()

        # set the gravity
        gravityFN = ForceNode('world-forces')
        gravityFNP = self.render.attachNewNode(gravityFN)
        gravityForce = LinearVectorForce(0, 0, -9.81)  # gravity acceleration
        gravityFN.addForce(gravityForce)
        self.physicsMgr.addLinearForce(gravityForce)

        # enable collision handling
        self.cTrav = CollisionTraverser('bullet sample traverser')
        # self.cTrav.showCollisions(self.render) # É ESTA LINHA CARALHOOOOOOO
        # print(self.cTrav.showCollisions(self.render))
        # self.cTrav.setRespectPrevTransform(True)
        self.pusher = PhysicsCollisionHandler()
        self.pusher.addInPattern('%fn-hit')

        self.accept("space", self.shoot)

        self.bulletIndex = 0
        self.bullets = []

        self.panda = self.loader.loadModel("models/panda")
        self.panda.reparentTo(self.render)
        self.panda.setCollideMask(BitMask32.bit(1))

        self.bulletIndex = 0
        self.bullets = []

        self.accept("space", self.shoot)

        self.create_pandas_runway()

    def shoot(self):
        self.bullets.append(self.shootBullet())

    def bulletHit(self, bulletAN, lvf, entry):
        # print(lvf)
        # print(type(bulletAN))
        # print(bulletAN.get_children())
        bulletAN.getPhysical(0).removeLinearForce(lvf)

    def shootBullet(self):
        # setup the base node for our bullet
        bulletNP = NodePath("Bullet-%02d" % self.bulletIndex)
        print(bulletNP.getName())
        self.bulletIndex += 1
        bulletNP.setPos(0, self.camera.getY(), 5)
        bulletNP.reparentTo(self.render)
        # create a node that will enable physics
        bulletAN = ActorNode("bullet-physics")
        # 3.3g
        bulletAN.getPhysicsObject().setMass(0.033)
        # attach the base node to the physics node
        # this will give us the following nodepath structure
        # render < bulletNP < bulletANP < bulletAN (actual node)
        bulletANP = bulletNP.attachNewNode(bulletAN)
        # attach the node also to the physic manager so it will be
        # affected by the physic simulation
        self.physicsMgr.attachPhysicalNode(bulletAN)
        # load a visual model to represent the bullet
        bullet = self.loader.loadModel("models/smiley")
        color = LPoint3f(1, 0, 0)
        bullet.setColor(color.getX(), color.getY(), color.getZ(), 1.0)
        bullet.reparentTo(bulletANP)
        tex = self.loader.loadTexture("maps/noise.rgb")
        bullet.setTexture(tex, 1)  # the second parameter is the priority

        # setup the collision detection
        bulletSphere = CollisionSphere(0, 0, 0, 1)
        bulletCollision = bulletANP.attachNewNode(CollisionNode("bulletCollision-%02d" % self.bulletIndex))
        bulletCollision.node().addSolid(bulletSphere)
        # bulletCollision.show()
        self.pusher.addCollider(bulletCollision, bulletANP)
        self.cTrav.addCollider(bulletCollision, self.pusher)

        bulletFN = ForceNode('Bullet-force')
        bulletFNP = bulletNP.attachNewNode(bulletFN)
        # 150 fps
        lvf = LinearVectorForce(0, 60, 0)
        lvf.setMassDependent(1)
        bulletFN.addForce(lvf)
        bulletAN.getPhysical(0).addLinearForce(lvf)

        self.accept("bulletCollision-%02d-hit" % self.bulletIndex, self.bulletHit, extraArgs=[bulletAN, lvf])

        self.taskMgr.doMethodLater(5, self.doRemove, 'doRemove',
                                   extraArgs=[bulletNP],
                                   appendTask=True)

        return bulletNP

    def doRemove(self, bulletNP, task):
        bulletNP.removeNode()
        self.bullets.remove(bulletNP)
        return task.done

    def create_floor(self):
        plane: NodePath = Plane(self.render, 12, 2.5, self.loader, "textures/neon.jpg").get_plane()
        plane.setPos(-4, -5, 0)
        print(plane.getPos())

    def create_pandas_runway(self):
        self.panda_runway = NodePath("panda_runway")
        panda_sample = self.loader.loadModel("models/panda")
        panda_sample.setScale(0.1, 0.1, 0.1)
        panda_sample.setH(90)
        counter = -10
        while counter < 0:
            panda_left = copy.deepcopy(panda_sample)
            panda_left.setPos(-5, counter, 0)
            panda_left.reparentTo(self.panda_runway)

            panda_right = copy.deepcopy(panda_sample)
            panda_right.setPos(-3, counter, 0)
            panda_right.setH(-90)
            panda_right.reparentTo(self.panda_runway)
            counter += 1.5
        self.panda_runway.reparentTo(self.render)


    # update loop
    def update(self, task):

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
