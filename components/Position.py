from pygame.math import Vector2
from ecs import Component

class PositionComponent(Component):
    def __init__(self, position=Vector2()):
        super(PositionComponent, self).__init__()
        self.value = position
