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
        self.entityCollisionSet = {}

    def getEntityCollisions(self, id):
        return self.entityCollisionSet[id]

    def process(self, entities, dt):
        # Dictionary to store items who we need to correct the physics of
        tileCollidedEntities = set()

        # Reset the entity collision sets for this frame.
        self.entityCollisionSet = {}

        # Reset our knowledge of which entities are in which tiles
        self.tileEntityMap = {}

        # Process entities
        for entity in entities:
            # Initalise the entityCollisionSet
            self.entityCollisionSet[entity.id] = set()

            # Retrieve relevant components
            positionComponent = entity.getComponent('Position')
            position = positionComponent.value
            collidable = entity.getComponent('Collidable')
            # Does entity have a size?
            dimension = entity.getComponent('Dimension').value \
                    if entity.hasComponent('Dimension') \
                    else Vector2(1, 1)

            # Calculate the number of tiles entity overlaps
            maxPosition = position + dimension
            startTileX = math.floor(position.x / self.tileMap.cellSize[0])
            startTileY = math.floor(position.y / self.tileMap.cellSize[1])
            startTile = Vector2(startTileX, startTileY)

            endTileX = math.ceil(maxPosition.x / self.tileMap.cellSize[0])
            endTileY = math.ceil(maxPosition.y / self.tileMap.cellSize[1])
            endTile = (endTileX, endTileY)

            tileDimensions = endTile - startTile

            # Test collisions in tiles which entity overlaps
            for x in range(int(tileDimensions.x)):
                for y in range(int(tileDimensions.y)):
                    tileX, tileY = Vector2(x, y) + startTile
                    tile = self.tileMap.getTileData(tileX, tileY, 0)
                    # Record the tile location for the entity
                    if (tileX, tileY) not in self.tileEntityMap:
                        self.tileEntityMap[tileX, tileY] = set()
                    self.tileEntityMap[tileX, tileY].add(entity)
                    if tile == 'SOLID' and entity.hasComponent('Velocity'):
                        tileCollidedEntities.add(entity)

        # Dispatch events and correct the physics
        # This method is really dumb and should be improved
        # for high-speed objects
        for entity in tileCollidedEntities:
            # Dispatch a collision event
            data = {'code': 'COLLISION', 'collisionType': 'tile' }
            event = pygame.event.Event(pygame.USEREVENT, data)
            entity.getComponent('Collidable').handle(event)
            # Correct entity position
            position = entity.getComponent('Position').value
            velocityComponent = entity.getComponent('Velocity')
            position -= velocityComponent.value
            velocityComponent.value = Vector2()

        # Process E-E collisions
        # This will eventually be refactored into its own system
        # For simplification reasons
        for key in self.tileEntityMap:
            entities = self.tileEntityMap[key]
            currentEntity = entities.pop()
            collidable = currentEntity.getComponent('Collidable')
            for other in entities:
                if other not in self.entityCollisionSet[currentEntity.id]:
                    self.entityCollisionSet[currentEntity.id].add(other)
                    data = { 'code': 'COLLISION', 'collisionType': 'entity', 'other': entity.id }
                    event = pygame.event.Event(pygame.USEREVENT, data)
                    collidable.handle(event)
                    other.getComponent('Collidable').handle(event)
