from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from panda3d.physics import ForceNode, LinearVectorForce, PhysicsCollisionHandler, ActorNode


class MyApp(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        # setup the camera

        # self.disableMouse()
        print(self.camera.getPos())
        # self.camera.setPos(0., -1050., 130.)
        # self.camera.setHpr(0., -30., 0.)

        # setup the lighting

        dir_light = DirectionalLight("dir_light")
        self.light = self.render.attachNewNode(dir_light)
        self.light.setColor((1., 1., 1., 1.))
        self.light.setHpr(45., -45., 0)
        self.render.setLight(self.light)

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
        bullet = self.loader.loadModel("smiley")
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



app = MyApp()
app.run()