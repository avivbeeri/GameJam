from ecs import System
import math
import newvector

class PhysicsSystem(System):

    def __init__(self):
        super(PhysicsSystem, self).__init__();
        self.requirements = ('Position', 'Acceleration', 'Velocity')

    def process(self, entities, dt):
        friction = 0
        # dt = (1.0 / 60.0)
        for entity in entities:
            positionComponent = entity.getComponent('Position')
            velocityComponent = entity.getComponent('Velocity')
            accelerationComponent = entity.getComponent('Acceleration')

            # TargetVelocity is read-only so we don't need its component.

            currentPosition = positionComponent.value
            currentVelocity = velocityComponent.value
            currentAcceleration = accelerationComponent.value

            # ----- Basic Kinematic - Disabled
            # x, y = currentAcceleration * targetVelocity + (1 - currentAcceleration) * currentVelocity


            # position += timestep * (velocity + timestep * acceleration / 2);
            # velocity += timestep * acceleration;


            # ----- Velocity Verlet Physics
            positionComponent.value += dt * (currentVelocity + dt * currentAcceleration / 2)
            velocityComponent.value += dt * currentAcceleration

            x, y = velocityComponent.value
            if (math.fabs(x) < 0.001): x = 0
            if (math.fabs(y) < 0.001): y = 0

            # Update components with new values
            velocityComponent.value = newvector.Vector2((x, y))
            positionComponent.value = currentPosition + velocityComponent.value
