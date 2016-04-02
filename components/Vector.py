from pygame.math import Vector2
from ecs import Component

class VectorComponent(Component):
    def __init__(self, vector=Vector2()):
        super(VectorComponent, self).__init__()
        self.value = Vector2(vector)
