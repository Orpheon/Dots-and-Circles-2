from __future__ import division

import math, random, pygame

from creature import Creature
from food import Food
from AI import neuralnet

class Game(object):
    NUM_CREATURES = 30
    NUM_FOOD = 50
    WINDOW_SIZE = (1280, 924)
    RENDERING_ON = True

    def __init__(self):
        self.creaturelist = []
        self.foodlist = []

        if self.RENDERING_ON:
            self.window = pygame.display.set_mode((self.WINDOW_SIZE[0], self.WINDOW_SIZE[1]+100))
            self.surface = pygame.display.get_surface()

        for i in range(self.NUM_CREATURES):
            Creature(self, neuralnet.NeuralNetwork(), random.randint(0, self.WINDOW_SIZE[0]), random.randint(0, self.WINDOW_SIZE[1]))

        for i in range(self.NUM_FOOD):
            Food(self, random.randint(0, self.WINDOW_SIZE[0]), random.randint(0, self.WINDOW_SIZE[1]))

    def step(self):
        pygame.event.clear()

        # Let each creature deacide and react
        for creature in self.creaturelist:
            creature.step(self)

        # Physics
        for creature in self.creaturelist:
            creature.endstep(self)
        for food in self.foodlist:
            food.endstep(self)

        # Render if rendering is enabled
        if self.RENDERING_ON:
            self.surface.fill((0, 0, 0))

            for creature in self.creaturelist:
                creature.render(self.surface)
            for food in self.foodlist:
                food.render(self.surface)

            pygame.display.flip()
