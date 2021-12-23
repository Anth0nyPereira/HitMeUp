from direct.showbase.ShowBase import ShowBase


class Game(ShowBase):
    def __init__(self):
        super(Game, self).__init__()


game = Game()
game.run()
