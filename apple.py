from panda3d.core import NodePath, Material, AmbientLight, PointLight


class Apple():
    def __init__(self, loader, color, render=None, is_intruder=False):  # color should be a Vec4
        # self.apple: NodePath = loader.loadModel("objects/apple.stl")
        self.apple: NodePath = loader.loadModel("models/panda")
        # print("apple is " +  str(type(self.apple)))
        # print("color in apple is " + str(color))
        # self.apple.setColor(color)
        # self.apple.setScale(0.02, 0.02, 0.02)
        self.apple.setScale(0.1, 0.1, 0.1)

        self.loader = loader
        self.render = render
        self.is_intruder = is_intruder

        # setting materials is not working also

        '''
        myMaterial = Material()
        myMaterial.setShininess(5.0)  # Make this material shiny
        myMaterial.setAmbient((0, 0, 1, 1))  # Make this material blue
        myMaterial.setShininess(0.128)
        self.apple.setMaterial(myMaterial)
        '''

    def set_light_to_apple(self):
        if self.is_intruder:
            self.alight2 = AmbientLight("alight")
            self.alight2.setColor((1, 0, 0, 1))
            self.alnp2 = self.render.attachNewNode(self.alight2)
            self.apple.setLight(self.alnp2)
        else:
            self.plight = PointLight("plight")
            self.plight.setColor((1, 0, 0, 1))
            self.plight_node = self.render.attachNewNode(self.plight)
            self.apple.setLight(self.plight_node)

    def set_texture_to_apple(self):
        tex = self.loader.loadTexture("textures/apple.jpg")
        self.apple.setTexture(tex, 1)  # the second parameter is the priority

    def get_apple(self):
        return self.apple
