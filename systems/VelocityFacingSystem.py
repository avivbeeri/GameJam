import pygame
from ecs import System
from util import Asset
from component import Facing

class VelocityFacingSystem(System):

    def __init__(self):
        super(VelocityFacingSystem, self).__init__()
        self.requirements = ('Drawable', 'Velocity', 'Facing')

    def process(self, entities, dt):
        for entity in entities:
            drawable = entity.getComponent("Drawable")
            velocity = entity.getComponent("Velocity").value
            facing = entity.getComponent("Facing")
            if velocity.x != 0:
                if velocity.x < 0:
                    facing.direction = Facing.LEFT
                else:
                    facing.direction = Facing.RIGHT

            drawable.flip(facing.direction is Facing.LEFT)
