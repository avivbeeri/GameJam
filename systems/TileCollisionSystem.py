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
        if id in self.entityCollisionSet:
            return self.entityCollisionSet[id]
        else:
            return []

    def getEntitiesInTile(self, x, y):
        if (x, y) in self.tileEntityMap:
            return self.tileEntityMap[int(x), int(y)]
        else:
            return []

    def getTilePosition(self, vector):
        tileX = math.floor(vector.x / self.tileMap.cellSize[0])
        tileY = math.floor(vector.y / self.tileMap.cellSize[1])
        return Vector2(tileX, tileY)

    def isRaycastClear(self, start, end):
        # Bresenham Algorithm
        # http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python
        solid = False
        tiles = []
        startTile = self.getTilePosition(start)
        endTile = self.getTilePosition(end)
        delta = endTile - startTile


        isSteep = abs(delta.y) > abs(delta.x)
        if isSteep:
            startTile.x, startTile.y = startTile.y, startTile.x
            endTile.x, endTile.y = endTile.y, endTile.x


        swapped = False
        if (startTile.x > endTile.x):
            startTile.x, endTile.x = endTile.x, startTile.x
            startTile.y, endTile.y = endTile.y, startTile.y

        delta = endTile - startTile
        error = int(delta.x / 2.0)
        y = startTile.y
        ystep = 1 if startTile.y < endTile.y else -1

        for x in range(int(startTile.x), int(endTile.x + 1)):
            coord = (y, x) if isSteep else (x, y)
            tiles.append(coord)
            tileX, tileY = coord
            tile = self.tileMap.getTileData(tileX, tileY, 0)
            if tile == 'SOLID':
                return False
            error -= abs(delta.y)
            while error < 0:
                y = y + ystep
                error += delta.x

        return True


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
            startTile = self.getTilePosition(position)

            # We can't refactor this calculation because we use math.ceil here.
            endTileX = math.ceil(maxPosition.x / self.tileMap.cellSize[0])
            endTileY = math.ceil(maxPosition.y / self.tileMap.cellSize[1])
            endTile = Vector2(endTileX, endTileY)

            # Test collisions in tiles which entity overlaps
            for tileX in range(int(startTile.x), int(endTile.x)):
                for tileY in range(int(startTile.y), int(endTile.y)):
                    tile = self.tileMap.getTileData(tileX, tileY, 0)
                    # Record the tile location for the entity
                    if (tileX, tileY) not in self.tileEntityMap:
                        self.tileEntityMap[tileX, tileY] = set()
                    self.tileEntityMap[tileX, tileY].add(entity)
                    if tile == 'SOLID':
                        tileCollidedEntities.add(entity)

        # Dispatch events and correct the physics
        # This method is really dumb and should be improved
        # for high-speed objects
        # NOTE: We currently don't update the tileEntityMap with physics corrections
        for entity in tileCollidedEntities:
            # Dispatch a collision event
            data = {'code': 'COLLISION', 'collisionType': 'tile' }
            event = pygame.event.Event(pygame.USEREVENT, data)
            entity.getComponent('Collidable').handle(event)
            if entity.hasComponent('Velocity'):
                # Correct entity position
                positionComponent = entity.getComponent('Position')
                position = positionComponent.value
                velocityComponent = entity.getComponent('Velocity')
                position -= velocityComponent.value
                velocityComponent.value = Vector2()
            elif entity.hasComponent('LastPosition'):
                positionComponent.value = Vector2(entity.getComponent('LastPosition').value)

        # Process E-E collisions
        # This will eventually be refactored into its own system
        # For simplification reasons
        for key in self.tileEntityMap:
            checkedEntities = set()
            entities = self.tileEntityMap[key]
            while len(entities) > 1:
                currentEntity = entities.pop()
                checkedEntities.add(currentEntity)
                for other in entities:
                    if other not in self.entityCollisionSet[currentEntity.id] and \
                        areEntitiesColliding(currentEntity, other):
                        # Check if the two entities are actually colliding
                        self.entityCollisionSet[currentEntity.id].add(other)
                        self.entityCollisionSet[other.id].add(currentEntity)
                        data = { 'code': 'COLLISION', 'collisionType': 'entity', 'other': entity.id }
                        event = pygame.event.Event(pygame.USEREVENT, data)
                        currentEntity.getComponent('Collidable').handle(event)
                        other.getComponent('Collidable').handle(event)
                self.tileEntityMap[key] = checkedEntities


def areEntitiesColliding(entity1, entity2):
    position1 = entity1.getComponent('Position').value
    dimension1 = getEntityDimension(entity1)
    position2 = entity2.getComponent('Position').value
    dimension2 = getEntityDimension(entity2)

    return (position1.x < position2.x + dimension2.x) and \
        (position1.x + dimension1.x > position2.x) and \
        (position1.y < position2.y + dimension2.y) and \
        (position1.y + dimension1.y > position2.y)

def getEntityDimension(entity):
    return entity.getComponent('Dimension').value \
            if entity.hasComponent('Dimension') \
            else Vector2(0, 0)
