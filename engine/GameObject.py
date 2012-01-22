from __future__ import division

class GameObject(object):
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.color = (0, 0, 0)
        self.width = 0

    def endstep(self, game):
        # The world isn't frictionless
        self.hspeed -= math.copysign(game.GLOBAL_DRAG, self.hspeed)
        self.vspeed -= math.copysign(game.GLOBAL_DRAG, self.vspeed)

        # Move
        self.x += self.hspeed
        self.y += self.vspeed

        # Make the borders of the game go in one-another (the world is toridal)
        if self.x < 0:# Exceeded left border
                self.x = game.surface.get_width()-self.x
        elif self.x > game.surface.get_width():# Exceeded right border
                self.x = self.x-game.surface.get_width()

        if self.y < 0:# Exceeded top border
                self.y = game.surface.get_height()-self.y
        elif self.y > game.surface.get_height():# Exceeded bottom border
                self.y = self.y-game.surface.get_height()
