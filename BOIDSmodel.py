from random import random


class Food:
    def __init__(self, x, y, amount=10):
        self.x = x
        self.y = y
        self.amount = amount


class Pheromone:
    def __init__(self, x, y, strength=1.0):
        self.x = x
        self.y = y
        self.strength = strength

    def evaporate(self, m=0.99):
        self.strength *= self.strength > 0.01 and m or 0

class Ant:
    def __init__(self, colony, x, y):
        self.colony = colony
        self.x = x
        self.y = y
        self.v = [0, 0]
        self.food = False
        self.trail = []
        self.roaming = random() * 100


def distance(v1, v2):
    return ((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2) ** 0.5


def steer(ant, target):
        d = distance(ant, target) + 0.0001
        ant.v[0] = (target.x - ant.x) / d
        ant.v[1] = (target.y - ant.y) / d
        ant.roaming = 0


def pheromones(colony):
    for ant in colony.ants:
        for pheromone in ant.trail:
            yield pheromone


def roam(ant, m=0.3):
    ant.v[0] += m * (random() * 2 - 1)
    ant.v[1] += m * (random() * 2 - 1)
    ant.roaming += 1
    if ant.roaming > ant.colony.radius:
        steer(ant, ant.colony)
    if distance(ant, ant.colony) < 10:
            ant.roaming = 0


def track(ant):
    for pheromone in pheromones(ant.colony):
        if distance(ant, pheromone) < pheromone.strength * 30:
            if random() < pheromone.strength:
                steer(ant, pheromone)
                return


def harvest(ant):
    for food in ant.colony.foodsources:
        if distance(ant, food) < max(1, food.amount / 2):
            food.amount -= 1
            if food.amount <= 0:
                ant.colony.foodsources.remove(food)
                ant.trail = []
            ant.trail.append(Pheromone(food.x, food.y))
            ant.trail.append(Pheromone(ant.x, ant.y))
            ant.food = True


def hoard(ant, m=0.5):
    steer(ant, ant.colony)
    if random() < m:
        ant.trail.append(Pheromone(ant.x, ant.y))
        if distance(ant, ant.colony) < 5:
            ant.food = False
            ant.colony.food += 1

def forage(ant, speed=1):
    if ant.food is False:
        roam(ant); track(ant); harvest(ant)
    else:
        hoard(ant)
    ant.v[0] = max(-speed, min(ant.v[0], speed))
    ant.v[1] = max(-speed, min(ant.v[1], speed))
    ant.x += ant.v[0]
    ant.y += ant.v[1]


class Colony:
    def __init__(self, x, y, radius=200, size=30):
        self.x = x
        self.y = y
        self.radius = radius
        self.foodsources = []
        self.food = 0
        self.ants = [Ant(self, x, y) for i in range(size)]

    def update(self, speed=1):
        for ant in self.ants:
            for pheromone in ant.trail:
                pheromone.evaporate()
                if pheromone.strength == 0:
                    ant.trail.remove(pheromone)
            forage(ant, speed)

# insert path to nodebox
# MODULE = ''
import sys;
if MODULE not in sys.path:
    sys.path.append(MODULE)
from nodebox.graphics import *

colony = Colony(200, 200, size=30)
colony.foodsources = [Food(random() * 400, random() * 400) for i in range(10)]


def draw(canvas):
    canvas.clear()
    for food in colony.foodsources:
        r = food.amount
        ellipse(food.x-r, food.y-r, r*2, r*2)
    for ant in colony.ants:
        ellipse(ant.x-1, ant.y-1, 2, 2)
    colony.update()

canvas.size = 400, 400
canvas.draw = draw
canvas.run()
