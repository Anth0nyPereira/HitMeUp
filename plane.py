from panda3d.core import CardMaker, NodePath


class Plane:
    def __init__(self, render, width, height, loader=None, texture=None):

        self.render = render
        self.loader = loader

        # initialize plane
        self.plane = CardMaker("plane")

        # set the size of the card (left, right, bottom, top - in XZ-plane)
        self.plane.setFrame(-width / 2, width / 2, -height / 2, height / 2)
        self.plane_node = self.render.attachNewNode(self.plane.generate())
        self.plane_node.setH(90)
        self.plane_node.setP(-90)

        # the card is created vertically in the XZ-plane, so it has to be rotated
        # to make it horizontal
        # self.plane_node.setP(-90.)

        if loader != None and texture != None:
            road_tex = loader.loadTexture(texture)
            self.plane_node.setTexture(road_tex)
            print("texture was set")

    def get_plane(self):
        return self.plane_node
