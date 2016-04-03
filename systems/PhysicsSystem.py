from ecs import System
import math
import pygame.math

class PhysicsSystem(System):

    def __init__(self):
        super(PhysicsSystem, self).__init__();
        self.requirements = ('Position', 'Acceleration', 'Velocity')

    def process(self, entities):
        friction = 0
        dt = (1.0 / 60.0)
        for entity in entities:
            positionComponent = entity.getComponent('Position')
            velocityComponent = entity.getComponent('Velocity')
            accelerationComponent = entity.getComponent('Acceleration')

            # TargetVelocity is read-only so we don't need its component.
            targetVelocity = entity.getComponent('TargetVelocity').value

            currentPosition = positionComponent.value
            currentVelocity = velocityComponent.value
            currentAcceleration = accelerationComponent.value

            # Update components with new values
            velocityComponent.value = pygame.math.Vector2((x, y))
            positionComponent.value = currentPosition + velocityComponent.value
