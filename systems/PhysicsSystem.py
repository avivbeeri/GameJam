from ecs import System

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
            currentPosition = positionComponent.value
            currentVelocity = velocityComponent.value
            currentAcceleration = accelerationComponent.value

            #   Velocity Verlot Method:
            #s   http://gamedev.stackexchange.com/questions/15708/how-can-i-implement-gravity

            newPosition = currentPosition + dt * (currentVelocity + dt * currentAcceleration / 2)
            newVelocity = currentVelocity + dt * currentAcceleration

            # Update components with new values
            positionComponent.value = newPosition
            velocityComponent.value = newVelocity
