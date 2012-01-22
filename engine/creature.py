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
        self.leftimage = []
        self.rightimage = []

    def step(self, game):
        # Get the new eye positions
        x1 = self.x + math.sin(self.direction)*self.EYE_SEPARATION/2
        y1 = self.y + math.cos(self.direction)*self.EYE_SEPARATION/2
        x2 = self.x + math.sin(self.direction)*self.EYE_SEPARATION/-2
        y2 = self.y+ math.cos(self.direction)*self.EYE_SEPARATION/-2

        # Put the eyes there
        self.lefteye.update(x1, y1, self.direction)
        self.righteye.update(x2, y2, self.direction)

        # Look at the world through them
        self.leftimage = self.lefteye.render(game)
        self.rightimage = self.righteye.render(game)

        # Interpret that world, and give some action
        # FIXME: DISABLED
        motorleft, motorright = self.brain.process(self.leftimage, self.rightimage)

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
        # Main body
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.size)

        # Line pointing in direction
        pygame.draw.line(surface, (255, 0, 0), (int(self.x), int(self.y)), (int(self.x+self.hspeed*10), int(self.y+self.vspeed*10)))

        # Eye positions
        x1 = self.x + math.sin(self.direction)*self.EYE_SEPARATION/2
        y1 = self.y + math.cos(self.direction)*self.EYE_SEPARATION/2
        x2 = self.x + math.sin(self.direction)*self.EYE_SEPARATION/-2
        y2 = self.y + math.cos(self.direction)*self.EYE_SEPARATION/-2

        # Draw the eyes
        pygame.draw.circle(surface, (255, 255, 0), (int(x1), int(y1)), 2)
        pygame.draw.circle(surface, (255, 255, 0), (int(x2), int(y2)), 2)

        # Draw what the creature sees
        pygame.draw.rect(surface, (255, 255, 255), pygame.rect.Rect(0, surface.get_height()-100, surface.get_width(), surface.get_height()), 1)
        compartiment_size = surface.get_width()/len(self.leftimage)

        for raw_color in self.leftimage:
            if raw_color == self.COLOR_NOTHING:
                color = (0, 0, 0)
            elif raw_color == self.COLOR_CREATURE:
                color = (255, 0, 0)
            elif raw_color == self.COLOR_FOOD:
                color = (0, 255, 0)

            offset = self.leftimage.index(raw_color) * compartiment_size
            rect = pygame.rect.Rect(offset, surface.get_height()-100, offset+compartiment_size, surface.get_height())
            pygame.draw.rect(surface, color, rect)
