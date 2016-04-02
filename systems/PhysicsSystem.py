from ecs import System

class PhysicsSystem(System):

    def __init__(self):
        super(PhysicsSystem, self).__init__();
        self.requirements = ('PositionComponent', 'AccelerationComponent', 'VelocityComponent')

    def process(self, entities):
        friction = 0
        dt = (1.0 / 60.0)
        for entity in entities:
            positionComponent = entity.getComponent('PositionComponent')
            velocityComponent = entity.getComponent('VelocityComponent')
            accelerationComponent = entity.getComponent('AccelerationComponent')
            currentPosition = positionComponent.value
            currentVelocity = velocityComponent.value
            currentAcceleration = accelerationComponent.value

            '''
                Velocity Verlot Method:
                http://gamedev.stackexchange.com/questions/15708/how-can-i-implement-gravity
            '''

            newPosition = currentPosition + dt * (currentVelocity + dt * currentAcceleration / 2)
            newVelocity = currentVelocity + dt * currentAcceleration

            # Update components with new values
            positionComponent.value = newPosition
            velocityComponent.value = newVelocity
