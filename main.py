from panda3d.core import loadPrcFile # funct import to load configurations file
from direct.showbase.ShowBase import ShowBase

loadPrcFile("config/conf.prc")

class Game(ShowBase):
    def __init__(self):
        super(Game, self).__init__()


game = Game()

# print(__builtins__.camera)

game.run()
