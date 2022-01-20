from panda3d.core import LineSegs, Vec4, NodePath

class AxisHelper():
    def __init__(self, length):
        # making the first-X axis
        self.axis_X = LineSegs()
        self.axis_X.setThickness(2.0)
        self.axis_X.setColor(Vec4(1, 0, 0, 1))
        self.axis_X.moveTo(-length, 0, 0)
        self.axis_X.drawTo(length, 0, 0)

        # now the Y-axis, note that in panda3d it switched with the Z one
        self.axis_Y = LineSegs()
        self.axis_Y.setThickness(2.0)
        self.axis_Y.setColor(Vec4(0, 1, 0, 1))
        self.axis_Y.moveTo(0, -length, 0)
        self.axis_Y.drawTo(0, length, 0)

        # Z-axis
        self.axis_Z = LineSegs()
        self.axis_Z.setThickness(2.0)
        self.axis_Z.setColor(Vec4(0, 0, 1, 1))
        self.axis_Z.moveTo(0, 0, -length)
        self.axis_Z.drawTo(0, 0, length)

        # create empty nodepath to store the 3 axis
        self.empty = NodePath("empty")

        # create nodes for each axis
        self.node_axis_X = self.axis_X.create(1)
        self.node_axis_Y = self.axis_Y.create(1)
        self.node_axis_Z = self.axis_Z.create(1)

        # attach to empty/parent
        print(type(self.empty))
        print(type(self.node_axis_X))
        self.empty.attachNewNode(self.node_axis_X)
        self.empty.attachNewNode(self.node_axis_Y)
        self.empty.attachNewNode(self.node_axis_Z)

    def get_axis(self):
        return self.empty


