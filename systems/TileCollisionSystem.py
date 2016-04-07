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
        collidedEntities = set()
        for entity in entities:
            positionComponent = entity.getComponent('Position')
            position = positionComponent.value
            collidable = entity.getComponent('Collidable')

            # Does entity have a size?
            dimension = entity.getComponent('Dimension').value \
                    if entity.hasComponent('Dimension') \
                    else Vector2(1, 1)

            maxPosition = position + dimension # This might be 1 pixel too big?

            startTileX = math.floor(position.x / self.tileMap.cellSize[0])
            startTileY = math.floor(position.y / self.tileMap.cellSize[1])
            startTile = Vector2(startTileX, startTileY)

            endTileX = math.ceil(maxPosition.x / self.tileMap.cellSize[0])
            endTileY = math.ceil(maxPosition.y / self.tileMap.cellSize[1])
            endTile = (endTileX, endTileY)

            tileDimensions = endTile - startTile

            # Calculate tiles which entity overlaps.
            for x in range(int(tileDimensions.x)):
                for y in range(int(tileDimensions.y)):
                    tileX, tileY = Vector2(x, y) + startTile
                    tile = self.tileMap.getTileData(tileX, tileY, 0)
                    tileIndex = y * self.tileMap.mapSize[0] + x
                    if not tileIndex in tileEntityMap:
                        tileEntityMap[tileIndex] = set()
                    tileEntityMap[tileIndex].add(entity)
                    if tile == 'SOLID':
                        collidedEntities.add(entity)
                        # Dispatch a collision event
                        data = {'code': 'COLLISION', 'collisionType': 'tile', 'other': (tileX, tileY), }
                        event = pygame.event.Event(pygame.USEREVENT, data)
                        collidable.handle(event)

        # Correct the entity position
        # This method is really dumb and imperfect
        for entity in collidedEntities:
            if entity.hasComponent('Velocity'):
                velocityComponent = entity.getComponent('Velocity')
                position -= velocityComponent.value
                velocityComponent.value = Vector2()

        for key in tileEntityMap:
            entities = tileEntityMap[key]
            currentEntity = entities.pop()
            collidable = currentEntity.getComponent('Collidable')
            for other in entities:
                data = { 'code': 'COLLISION', 'collisionType': 'entity', 'other': other }
                event = pygame.event.Event(pygame.USEREVENT, data)
                collidable.handle(event)
