from __future__ import division

import math, pygame

from gameobject import GameObject
from food import Food
from AI import eye
from AI import neuralnet

class Creature(GameObject):
    MAX_SPEED = 5
    MAX_TURN_SPEED = 0.3
    EYE_SEPARATION = 15
    COLOR_NOTHING = 0
    COLOR_CREATURE = -1
    COLOR_FOOD = 1
    def __init__(self, game, brain,  x, y):
        GameObject.__init__(self, game, x, y)
        game.creaturelist.append(self)
        self.size = 10
        self.score = 0
        self.direction = 0
        self.brain = brain
        self.lefteye = eye.Eye(self, game)
        self.righteye = eye.Eye(self, game)

    def step(self, game):
        # Get the new eye positions
        x1 = math.sin(self.direction)*self.EYE_SEPARATION/2
        y1 = math.cos(self.direction)*self.EYE_SEPARATION/2
        x2 = math.sin(self.direction)*self.EYE_SEPARATION/-2
        y2 = math.cos(self.direction)*self.EYE_SEPARATION/-2

        # Put the eyes there
        self.lefteye.update(x1, y1, self.direction)
        self.righteye.update(x2, y2, self.direction)

        # Look at the world through them
        leftimage = self.lefteye.render(game)
        rightimage = self.righteye.render(game)

        # Interpret that world, and give some action
        # FIXME: DISABLED
        motorleft, motorright = 1, 1#self.brain.process(leftimage, rightimage)

        # Turn the tank
        rotation = motorleft-motorright # Get the direction changes
        rotation = min(self.MAX_TURN_SPEED, max(self.MAX_TURN_SPEED*(-1), rotation)) # Clamp to the max rotation
        self.direction = (self.direction+rotation) % 360 # Add the rotation to the self.direction

        # Update the speed
        self.speed = min(self.MAX_SPEED, max(self.MAX_SPEED*(-1), motorleft + motorright))

        # Translate it into hspeed and vspeed
        self.hspeed = math.cos(self.direction)*self.speed
        self.vspeed = math.sin(self.direction)*self.speed

        # If collides with food
        for food in game.foodlist:
            if math.hypot(self.x-food.x, self.y-food.y) < self.size+food.size:
                # Eat
                self.score += 1

    def destroy(self, game):
        self.lefteye = None
        self.righteye = None
        self.brain = None
        game.creaturelist.remove(self)


    def render(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.size)
        pygame.draw.line(surface, (255, 0, 0), (int(self.x), int(self.y)), (int(self.x+self.hspeed), int(self.y+self.vspeed)))
