from panda3d.core import NodePath, AmbientLight, Material

from color import Color


class BoxGeometry:

    def __init__(self, render, loader, width, depth, height):
        self.loader = loader
        self.render = render
        self.box_geometry: NodePath = self.loader.loadModel("models/box")
        self.box_geometry.setScale(width, depth, height)
        self.box_geometry.setZ(-0.3) # just because the object is even a little bit thick so
        self.texture = self.loader.loadTexture("textures/neon.jpg")
        self.box_geometry.setTexture(self.texture, 1)

        self.alight = AmbientLight("alight")
        self.alight.setColor((0.3, 0.3, 0.3, 1))
        self.alnp = self.render.attachNewNode(self.alight)
        self.box_geometry.setLight(self.alnp)

        box_material = Material()
        box_material.setAmbient((1, 0.5, 0.5, 1))
        # box_material.setSpecular(Color.white.value)
        # box_material.setAmbient((0, 0, 1, 1))  # Make this material blue
        self.box_geometry.setMaterial(box_material)

    def get_box(self):
        return self.box_geometry
