from pygame import *
from ecs import Component

class DrawableComponent(Component):
    def __init__(self, surface, layer = 0):
        super(DrawableComponent, self).__init__()
        self.image = surface
        self.layer = layer
