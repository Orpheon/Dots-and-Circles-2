from __future__ import division

import math

class Eye(object):
    MAX_EYESIGHT = 5000
    FOV = 160
    def __init__(self, owner, game):
        self.owner = owner
        self.x = 0
        self.y = 0
        self.direction = 0

    def update(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def render(self, game):
        distances = [self.MAX_EYESIGHT+1]*360
        raw_image = [self.owner.COLOR_NOTHING]*360

        for creature in game.creaturelist:
            angle = math.atan2(creature.y-self.y, creature.x-self.x)
            angle = int(math.degrees(angle))
            distance = math.hypot(creature.x-self.x, creature.y-self.y)
            if distances[angle] > distance:# If the creature is nearer than the last object stored in that pixel
                distances[angle] = distance
                raw_image[angle] = self.owner.COLOR_CREATURE

        for food in game.foodlist:
            angle = math.atan2(food.y-self.y, food.x-self.x)
            angle = int(math.degrees(angle))
            distance = math.hypot(food.x-self.x, food.y-self.y)
            if distances[angle] > distance:# If the food is nearer than the last object stored in that pixel
                distances[angle] = distance
                raw_image[angle] = self.owner.COLOR_FOOD

        # Now remove anything not in the FOV
        start_angle = int(self.direction - self.FOV/2)
        stop_angle = int(start_angle + self.FOV)
        image = []

        for angle in range(start_angle, stop_angle):
            image.append(raw_image[angle % 360])

        return image
