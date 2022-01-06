from panda3d.core import NodePath, Material


class Apple():
    def __init__(self, loader, color):  # color should be a Vec4
        self.apple: NodePath = loader.loadModel("objects/apple.stl")
        # print("apple is " +  str(type(self.apple)))
        # print("color in apple is " + str(color))
        self.apple.setColor(color)
        self.apple.setScale(0.02, 0.02, 0.02)

        # setting materials is not working also
        '''
        myMaterial = Material()
        myMaterial.setShininess(5.0)  # Make this material shiny
        myMaterial.setAmbient((0, 0, 1, 1))  # Make this material blue
        myMaterial.setShininess(0.128)
        self.apple.setMaterial(myMaterial)
        '''


    def get_apple(self):
        return self.apple
