from __future__ import division

import math

class GameObject(object):
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.color = (0, 0, 0)
        self.width = 0

    def endstep(self, game):
        # Move
        self.x += self.hspeed
        self.y += self.vspeed

        # Make the borders of the game go in one-another (the world is toridal)
        if self.x < 0:# Exceeded left border
                self.x = game.WINDOW_SIZE[0]-self.x
        elif self.x > game.WINDOW_SIZE[0]:# Exceeded right border
                self.x = self.x-game.WINDOW_SIZE[0]

        if self.y < 0:# Exceeded top border
                self.y = game.WINDOW_SIZE[1]-self.y
        elif self.y > game.WINDOW_SIZE[1]:# Exceeded bottom border
                self.y = self.y-game.WINDOW_SIZE[1]
