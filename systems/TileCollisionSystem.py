# -*- coding: utf-8 -*-
from pygame.math import Vector2
import pygame
from ecs import System
import math


class TileCollisionSystem(System):

    def __init__(self, tileMap):
        super(TileCollisionSystem, self).__init__();
        self.requirements = ('Collidable', 'Position')
        self.tileMap = tileMap

    def process(self, entities, dt):
        tileEntityMap = {}
        # Events occurring in a given tile
        # Dictionary to store items who we need to correct the physics of
        collidedEntities = {}
        for entity in entities:
            positionComponent = entity.getComponent('Position')
            position = positionComponent.value
            collidable = entity.getComponent('Collidable')

            # Does entity have a size?
            dimension = entity.getComponent('Dimension').value \
                    if entity.hasComponent('Dimension') \
                    else Vector2()

            maxPosition = position + dimension # This might be 1 pixel too big?

            startTileX = int(position.x / self.tileMap.cellSize[0])
            startTileY = int(position.y / self.tileMap.cellSize[1])
            startTile = Vector2(startTileX, startTileY)

            endTileX = int(maxPosition.x / self.tileMap.cellSize[0])
            endTileY = int(maxPosition.y / self.tileMap.cellSize[1])

            # Calculate tiles which entity overlaps.
            for x in range(int(math.ceil(maxPosition.x / self.tileMap.cellSize[0]) - math.floor(position.x / self.tileMap.cellSize[0]))):
                for y in range(int(math.ceil(maxPosition.y / self.tileMap.cellSize[1]) - math.floor(position.y / self.tileMap.cellSize[1]))):
                    tileX, tileY = Vector2(x, y) + startTile
                    tile = self.tileMap.getTileData(tileX, tileY, 0)
                    tileIndex = y * self.tileMap.mapSize[0] + x
                    print tileIndex
                    if not tileIndex in tileEntityMap:
                        tileEntityMap[tileIndex] = set()
                    tileEntityMap[tileIndex].add(entity)
                    if tile == 'SOLID':
                        collidedEntities[entity.id] = entity
                        # Dispatch a collision event
                        data = {'code':'COLLISION', 'other': (tileX, tileY), 'type':'tile'}
                        event = pygame.event.Event(pygame.USEREVENT, data)
                        collidable.handle(event)
        # Correct the entity position
        # This method is really dumb and imperfect
        for key, entity in collidedEntities.items():
            if entity.hasComponent('Velocity'):
                velocityComponent = entity.getComponent('Velocity')
                position -= velocityComponent.value
                velocityComponent.value = Vector2()

        for key in tileEntityMap:
            entities = tileEntityMap[key]
            currentEntity = entities.pop()
            collidable = currentEntity.getComponent('Collidable')
            for other in entities:
                data = { 'code':"COLLISION", 'other': other, 'collisionType':'entity' }
                event = pygame.event.Event(pygame.USEREVENT, data)
                collidable.handle(event)
