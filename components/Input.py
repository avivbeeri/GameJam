from pygame.math import Vector2
from ecs import Component

class InputComponent(Component):
    def __init__(self):
        super(InputComponent, self).__init__()
        self.handlers = []

    def attachHandler(self, handler):
        self.handlers.append(handler)

    def process(self, keys):
        for handler in self.handlers:
            handler(self.entity, keys)
