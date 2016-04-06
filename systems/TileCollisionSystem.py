from pygame.math import Vector2
from ecs import System
import math

class TileCollisionSystem(System):

    def __init__(self, tileMap):
        super(TileCollisionSystem, self).__init__();
        self.requirements = ('Collidable', 'Position')
        self.tileMap = tileMap

    def process(self, entities, dt):
        collisionEvents = []
        for entity in entities:
            position = entity.getComponent('Position').value
            collidable = entity.getComponent('Collidable')

            # Does entity have a size?
            dimension = entity.getComponent('Dimension').value \
                    if entity.hasComponent('Dimension') \
                    else Vector2()

            maxPosition = position + dimension

            for x in range(int(math.ceil(maxPosition.x / self.tileMap.cellSize[0]) - math.floor(position.x / self.tileMap.cellSize[0]))):
                for y in range(int(math.ceil(maxPosition.y / self.tileMap.cellSize[1]) - math.floor(position.y / self.tileMap.cellSize[1]))):

                    tileX, tileY = Vector2(x, y) + (int(position.x / Vector2(self.tileMap.cellSize).x),int(position.y / Vector2(self.tileMap.cellSize).y))
                    tile = self.tileMap.getTileData(tileX, tileY, 0)
                    print (tileX, tileY, tile)
                    # print




            # Calculate tiles which entity overlaps.
