import copy
import math
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
from box_geometry import BoxGeometry
from bucket import Bucket
from color import Color
import random

from text import Text

loadPrcFile("config/conf.prc")

available_apples = []
timestamps = []


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        # create hallways
        self.create_hallways()

        # creating the intruder's game
        self.intruder_game = None
        self.score = 0
        self.set_intruder_game()
        self.score_obj = None
        self.score_text = None

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

        self.accept("space", self.update_key_map, ["shoot", True])

        self.accept("w-up", self.update_key_map, ["up", False])
        self.accept("s-up", self.update_key_map, ["down", False])
        self.accept("a-up", self.update_key_map, ["left", False])
        self.accept("d-up", self.update_key_map, ["right", False])

        self.accept("arrow_up-up", self.update_key_map, ["up", False])
        self.accept("arrow_down-up", self.update_key_map, ["down", False])
        self.accept("arrow_left-up", self.update_key_map, ["left", False])
        self.accept("arrow_right-up", self.update_key_map, ["right", False])

        self.accept("space-up", self.update_key_map, ["shoot", False])

        self.accept("mouse1", self.mouse_click)
        self.accept('wheel_up', self.zoom_in)
        self.accept('wheel_down', self.zoom_out)

        self.updateTask = self.taskMgr.add(self.update, "update")

        self.axis_helper = AxisHelper(10).get_axis()
        self.axis_helper.reparentTo(self.render)

        self.update_counter = 0

        self.last_mouse_position = Vec2(0, 0)

        self.camera.setPos(4, -18, 0.5)

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

        self.shooting_panda = self.create_card_maker()
        self.shooting_panda.setScale(0.25, 0.25, 0.25)
        self.shooting_panda.setX(-5)
        self.shooting_panda.setY(-1)
        self.shooting_panda.setH(90)

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
                self.camera.setH(self.camera.getH() * 8)
            else:
                self.camera.setH((self.camera.getH() + mpos.getX() * -1) * 8)

        if self.keyMap["up"]:
            self.camera.setY(self.camera, 15 * dt)
        if self.keyMap["down"]:
            self.camera.setY(self.camera, -15 * dt)
        if self.keyMap["left"]:
            self.camera.setX(self.camera, -10 * dt)
        if self.keyMap["right"]:
            self.camera.setX(self.camera, 10 * dt)

        return task.cont

    # this method will be called when the event of pressing one of the available keys will occur
    def update_key_map(self, key, value):
        self.keyMap[key] = value
        # print(controlName, "set to", controlState)

    def set_intruder_game(self):
        self.intruder_game = self.create_apples()
        self.intruder_game.setH(-90)
        self.intruder_game.setPos(10, 0, 0)
        self.intruder_game.setScale(0.7, 0.7, 0.7)

    def create_apples(self):
        score = self.score

        # create node that will store basically all the intruder game
        self.intruder_game = NodePath("intruder-game")

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
            apple.reparentTo(self.intruder_game)

            # create each bucket
            bucket: NodePath = Bucket(self.loader).get_bucket()
            bucket.setPos(pos, 0, 3)
            bucket.reparentTo(self.intruder_game)

            pos += 1

        # create labels
        self.correct = self.create_labels(self.intruder_game, "You got it right!", Color.green)
        self.correct.hide()
        self.correct.setPos(-0.5, 0, 3.5)
        self.wrong = self.create_labels(self.intruder_game, "Wrong, try again!", Color.red)
        self.wrong.setPos(-0.5, 0, 3.5)
        self.wrong.hide()
        self.score_label = self.create_labels(self.intruder_game, f"Score: {score}", Color.white)
        self.score_label.hide()
        self.intruder_game.reparentTo(self.render)
        return self.intruder_game

    def create_labels(self, intruder, message, color):

        # create text that will show if the response is correct or not
        score_obj = Text("label-%s" % message, message, color.value) # object
        score_text = score_obj.get_text() # TextNode
        score_np = intruder.attachNewNode(score_text)
        score_np.setScale(0.5)
        return score_np

    def hide_correct(self, task):
        self.correct.hide()
        return task.done

    def hide_wrong(self, task):
        self.wrong.hide()
        return task.done

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
                    self.correct.show()
                    self.taskMgr.doMethodLater(0.5, self.hide_correct, "hide-correct")
                    self.score += 1
                    pickedObj.detachNode()
                    pickedObj.removeNode()
                else:
                    print("Wrong, try again!")
                    self.wrong.show()
                    self.taskMgr.doMethodLater(0.5, self.hide_wrong, "hide-wrong")

    def add_shader2(self):
        print("entering add_shader2")
        # available_apples[0].node().setAttrib(ShadeModelAttrib.make(ShadeModelAttrib.MFlat)) # this doesnt work, go next
        # available_apples[1].node().setAttrib(ShadeModelAttrib.make(ShadeModelAttrib.MSmooth))

    def create_card_maker(self):
        # create empty node
        shooting_panda = NodePath("shooting-panda")

        # enable physics
        self.enableParticles()

        # create the plane
        cm = CardMaker("plane")
        # set the size of the card (left, right, bottom, top - in XZ-plane)
        cm.setFrame(-2, 2, -2, 2)
        self.plane = shooting_panda.attachNewNode(cm.generate())
        # the card is created vertically in the XZ-plane, so it has to be rotated
        # to make it horizontal
        # self.plane.setP(-90.)
        self.plane.setPos(0, -5, 10)
        self.plane.setCollideMask(BitMask32.bit(2))

        road_tex = self.loader.loadTexture("textures/sample.jpg")
        self.plane.setTexture(road_tex)

        # collision

        # set the gravity
        gravityFN = ForceNode('world-forces')
        gravityFNP = shooting_panda.attachNewNode(gravityFN)
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

        self.bulletIndex = 0
        self.bullets = []

        self.panda = self.loader.loadModel("models/panda")
        self.panda.reparentTo(shooting_panda)
        # self.panda.setCollideMask(BitMask32.bit(2))

        self.bulletIndex = 0
        self.bullets = []

        self.accept("space", self.shoot)
        shooting_panda.reparentTo(self.render)
        return shooting_panda

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
        bulletNP.setPos(0, self.camera.getY() - 50, 10)
        bulletNP.reparentTo(self.shooting_panda)
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
        # 60 fps
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

    def create_hallways(self):
        main_hallway = self.create_hallway(empty=False)
        right_hallway = self.create_hallway()
        right_hallway.setH(90)
        right_hallway.setPos(18, -3, 0)

        left_hallway = self.create_hallway()
        left_hallway.setH(-90)
        left_hallway.setPos(-10, 1, 0)
        left_hallway.setCollideMask(BitMask32.bit(2))

    def create_hallway(self, empty=True):

        # create pivot that will represent the whole object
        pivot = NodePath("pivot")
        pivot.setPos(2, -15, 0)
        pivot.reparentTo(self.render)

        if not empty:
            # create bears
            self.create_pandas_runway(pivot)

        width, depth, height = 4, 12, 0.3

        hall_bot: NodePath = BoxGeometry(self.loader, width, depth, height).get_box()
        hall_bot.reparentTo(pivot)

        hall_top: NodePath = BoxGeometry(self.loader, width, depth, height).get_box()
        hall_top.reparentTo(pivot)
        hall_top.setZ(4)

        hall_left: NodePath = BoxGeometry(self.loader, width, depth, height).get_box()
        hall_left.reparentTo(pivot)
        hall_left.setZ(4)
        hall_left.setR(90)

        hall_right: NodePath = BoxGeometry(self.loader, width, depth, height).get_box()
        hall_right.reparentTo(pivot)
        hall_right.setPos(3.7, 0, 4)
        hall_right.setR(90)
        return pivot

    def create_pandas_runway(self, pivot):
        self.panda_runway = NodePath("panda_runway")
        panda_sample = self.loader.loadModel("models/panda")
        panda_sample.setScale(0.1, 0.1, 0.15)
        panda_sample.setH(90)
        counter = 0
        while counter < 10:
            panda_left = copy.deepcopy(panda_sample)
            panda_left.setPos(0.5, counter, 0)
            panda_left.reparentTo(self.panda_runway)

            panda_right = copy.deepcopy(panda_sample)
            panda_right.setPos(3.5, counter, 0)
            panda_right.setH(-90)
            panda_right.reparentTo(self.panda_runway)
            counter += 1.5
        self.panda_runway.reparentTo(pivot)

    # update loop
    def update(self, task):

        # print(self.render.find("**/intruder-game").getChildren())

        # Get the amount of time since the last update
        dt = globalClock.getDt()
        # print(dt)
        timestamps.append(dt)
        if self.update_counter > 0 and self.update_counter % 5000 == 0:
            for i in range(len(available_apples)):
                available_apples[i].detachNode()
                available_apples[i].removeNode()
            available_apples.clear()
            # timestamps.clear()
            self.correct.hide()
            self.wrong.hide()
            self.set_intruder_game()
            # print(self.score)

        self.update_counter += 1
        return task.cont  # task.cont exists to make this task run forever


game = Game()

# print(__builtins__.camera)

game.run()
