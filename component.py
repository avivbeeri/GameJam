from pygame import *
from pygame.math import Vector2
from ecs import Component

class Vector(Component):
    def __init__(self, vector=Vector2()):
        super(Vector, self).__init__()
        self.value = Vector2(vector)

class Acceleration(Vector):
    pass

class Position(Vector):
    pass

class Velocity(Vector):
    pass

class Drawable(Component):
    def __init__(self, surface, layer = 0):
        super(Drawable, self).__init__()
        self.image = surface
        self.layer = layer

class Input(Component):
    def __init__(self):
        super(Input, self).__init__()
        self.handlers = []

    def attachHandler(self, handler):
        self.handlers.append(handler)

    def process(self, keys):
        for handler in self.handlers:
            handler(self.entity, keys)