from panda3d.core import NodePath


class BoxGeometry:

    def __init__(self, loader, width, depth, height):
        self.loader = loader
        self.box_geometry: NodePath = self.loader.loadModel("models/box")
        self.box_geometry.setScale(width, depth, height)
        self.box_geometry.setZ(-0.3) # just because the object is even a little bit thick so

    def get_box(self):
        return self.box_geometry
