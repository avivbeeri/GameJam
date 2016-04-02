from pygame import *
from ecs import Component

class DrawableComponent(Component):
    def __init__(self, surface):
        super(DrawableComponent, self).__init__()
        self.image = surface
