from __future__ import division

import pygame

from gameobject import GameObject

class Food(GameObject):
    def __init__(self, game, x, y):
        GameObject.__init__(self, game, x, y)
        game.foodlist.append(self)
        self.size = 5

    def destroy(self, game):
        game.foodlist.remove(self)

    def render(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), (int(self.x), int(self.y)), self.size)
