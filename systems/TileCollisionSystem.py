from pygame.math import Vector2
from ecs import System
import math

class TileCollisionSystem(System):

    def __init__(self, tileMap):
        super(TileCollisionSystem, self).__init__();
        self.requirements = ('Collidable', 'Position', 'Velocity')
        self.tileMap = tileMap

    def process(self, entities, dt):
        collisionEvents = []
        for entity in entities:
            positionComponent = entity.getComponent('Position')
            position = positionComponent.value
            velocityComponent = entity.getComponent('Velocity')
            collidable = entity.getComponent('Collidable')

            # Does entity have a size?
            dimension = entity.getComponent('Dimension').value \
                    if entity.hasComponent('Dimension') \
                    else Vector2()

            maxPosition = position + dimension # This might be 1 pixel too big?

            # Calculate tiles which entity overlaps.
            for x in range(int(math.ceil(maxPosition.x / self.tileMap.cellSize[0]) - math.floor(position.x / self.tileMap.cellSize[0]))):
                for y in range(int(math.ceil(maxPosition.y / self.tileMap.cellSize[1]) - math.floor(position.y / self.tileMap.cellSize[1]))):

                    tileX, tileY = Vector2(x, y) + (int(position.x / Vector2(self.tileMap.cellSize).x),int(position.y / Vector2(self.tileMap.cellSize).y))
                    tile = self.tileMap.getTileData(tileX, tileY, 0)
                    if tile == 'SOLID':
                        position -= velocityComponent.value
                        velocityComponent.value = Vector2()
