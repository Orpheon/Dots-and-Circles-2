from __future__ import division

import math

class Eye(object):
    MAX_EYESIGHT = 500
    FOV = 160
    IMAGE_RESOLUTION = 360
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
        distances = []
        raw_image = {}
        for i in range(self.IMAGE_RESOLUTION):
            distances.append(self.MAX_EYESIGHT+1)
            raw_image[i] = self.owner.COLOR_NOTHING

        for creature in game.creaturelist:
            angle = math.atan2(creature.y-self.y, creature.x-self.x)
            angle = int(math.degrees(angle)*self.IMAGE_RESOLUTION/360)
            distance = math.hypot(creature.x-self.x, creature.y-self.y)
            if distances[angle] > distance:# If the creature is nearer than the last object stored in that pixel
                distances[angle] = distance
                raw_image[angle] = self.owner.COLOR_CREATURE

        for food in game.foodlist:
            angle = math.atan2(food.y-self.y, food.x-self.x)
            angle = int(math.degrees(angle)*self.IMAGE_RESOLUTION/360)
            distance = math.hypot(food.x-self.x, food.y-self.y)
            if distances[angle] > distance:# If the food is nearer than the last object stored in that pixel
                distances[angle] = distance
                raw_image[angle] = self.owner.COLOR_FOOD

        # Now remove anything not in the FOV, and store what is in a list
        offset = self.FOV/-2
        image = []
        for i in range(self.FOV):
            image.append(raw_image[clock_add(i, offset)])

        return image



def clock_add(a, b, min=0, max=360):
    c = a+b
    while c < min:
        c += max-min
    while c > max:
        c -= max-min
    return c
