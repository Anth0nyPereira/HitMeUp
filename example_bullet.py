"""Simulate a bullet using panda3d's internal physic system"""


from direct.showbase.ShowBase import ShowBase
import sys

from direct.task.TaskManagerGlobal import taskMgr
from panda3d.physics import ForceNode
from panda3d.physics import LinearVectorForce
from panda3d.physics import ActorNode
from panda3d.physics import PhysicsCollisionHandler
from panda3d.core import NodePath
from panda3d.core import LPoint3f, Point3, Vec3
from panda3d.core import CollisionSphere
from panda3d.core import CollisionPlane
from panda3d.core import CollisionNode
from panda3d.core import CollisionTraverser
from panda3d.core import Plane

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # accept the esc button to close the application
        self.accept("escape", sys.exit)

        # enable physics
        self.enableParticles()

        # set the gravity
        gravityFN=ForceNode('world-forces')
        gravityFNP=self.render.attachNewNode(gravityFN)
        gravityForce=LinearVectorForce(0,0,-9.81) #gravity acceleration
        gravityFN.addForce(gravityForce)
        self.physicsMgr.addLinearForce(gravityForce)

        # enable collision handling
        self.cTrav = CollisionTraverser('bullet sample traverser')
        # self.cTrav.showCollisions(self.render) # É ESTA LINHA CARALHOOOOOOO
        # print(self.cTrav.showCollisions(self.render))
        # self.cTrav.setRespectPrevTransform(True)
        self.pusher = PhysicsCollisionHandler()
        self.pusher.addInPattern('%fn-hit')

        # setup a room which the bullet can collide with
        GroundPlane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, -25)))
        WallNPlane = CollisionPlane(Plane(Vec3(0, -1, 0), Point3(0, 25, 0)))
        WallEPlane = CollisionPlane(Plane(Vec3(-1, 0, 0), Point3(25, 0, 0)))
        WallSPlane = CollisionPlane(Plane(Vec3(0, 1, 0), Point3(0, -25, 0)))
        WallWPlane = CollisionPlane(Plane(Vec3(1, 0, 0), Point3(-25, 0, 0)))
        room = self.render.attachNewNode(CollisionNode('roomCollision'))
        # print(type(room.node()))
        room.node().addSolid(GroundPlane)
        room.node().addSolid(WallNPlane)
        room.node().addSolid(WallEPlane)
        room.node().addSolid(WallSPlane)
        room.node().addSolid(WallWPlane)
        room.show()

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
        self.bulletIndex += 1
        bulletNP.setPos(0, 0, 0)
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
        color=LPoint3f(1,0,0)
        bullet.setColor(color.getX(),color.getY(),color.getZ(),1.0)
        bullet.reparentTo(bulletANP)

        # setup the collision detection
        bulletSphere = CollisionSphere(0, 0, 0, 1)
        bulletCollision = bulletANP.attachNewNode(CollisionNode("bulletCollision-%02d" % self.bulletIndex))
        bulletCollision.node().addSolid(bulletSphere)
        # bulletCollision.show()
        self.pusher.addCollider(bulletCollision, bulletANP)
        self.cTrav.addCollider(bulletCollision, self.pusher)

        bulletFN = ForceNode('Bullet-force')
        bulletFNP = bulletNP.attachNewNode(bulletFN)
        # 214fps
        lvf = LinearVectorForce(0,214,0)
        lvf.setMassDependent(1)
        bulletFN.addForce(lvf)
        bulletAN.getPhysical(0).addLinearForce(lvf)

        self.accept("bulletCollision-%02d-hit" % self.bulletIndex, self.bulletHit, extraArgs=[bulletAN, lvf])

        taskMgr.doMethodLater(5, self.doRemove, 'doRemove',
            extraArgs=[bulletNP],
            appendTask=True)

        return bulletNP

    def doRemove(self, bulletNP, task):
        bulletNP.removeNode()
        self.bullets.remove(bulletNP)
        return task.done

world = Main()
world.run()