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
        self.tileEntityMap = {}

    def process(self, entities, dt):
        # Events occurring in a given tile
        # Dictionary to store items who we need to correct the physics of
        tileCollidedEntities = set()
        self.tileEntityMap = {}
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
                    # tileIndex = tileY * self.tileMap.mapSize[0] + tileX
                    if not (tileX, tileY) in self.tileEntityMap:
                        self.tileEntityMap[tileX, tileY] = set()
                    self.tileEntityMap[tileX, tileY].add(entity)
                    if tile == 'SOLID':
                        tileCollidedEntities.add(entity)


        # Correct the entity position
        # This method is really dumb and should be improved
        # for high-speed objects
        for entity in tileCollidedEntities:
            # Dispatch a collision event
            position = entity.getComponent('Position').value
            collidable = entity.getComponent('Collidable')
            data = {'code': 'COLLISION', 'collisionType': 'tile' }
            event = pygame.event.Event(pygame.USEREVENT, data)
            collidable.handle(event)
            if entity.hasComponent('Velocity'):
                velocityComponent = entity.getComponent('Velocity')
                position -= velocityComponent.value
                velocityComponent.value = Vector2()

        # Process E-E collisions
        collisions = set()
        for key in self.tileEntityMap:
            entities = self.tileEntityMap[key]
            currentEntity = entities.pop()
            collidable = currentEntity.getComponent('Collidable')
            for other in entities:
                collision = (currentEntity, other) if currentEntity.id < other.id else (other, currentEntity)
                if not collision in collisions:
                    data = { 'code': 'COLLISION', 'collisionType': 'entity', 'other': collision }
                    event = pygame.event.Event(pygame.USEREVENT, data)
                    collidable.handle(event)
                    other.getComponent('Collidable').handle(event)
