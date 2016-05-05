# System-wide imports
import pygame, os
from pytmx.util_pygame import load_pygame
from collections import OrderedDict
from util import Sprite

# Our other files
import maze, component

def create(world, **kwargs):
    '''
    A function to create an entity, designed to make game.py smaller and easier to read.
    Accepted kwargs are: position, sprite, layer, script, attachClass, classArgs, dimension
    '''
    entity = world.createEntity()
    if 'position' in kwargs:
        entity.addComponent(component.Position(kwargs['position']))
    if 'lastPosition' in kwargs:
        entity.addComponent(component.LastPosition(kwargs['lastPosition']))

    if 'sprite' in kwargs:
        if 'layer' not in kwargs:
            kwargs['layer'] = 0
        if 'offset' not in kwargs:
            kwargs['offset'] = (0, 0)
        kwargs['sprite'] = Sprite(kwargs['sprite'])
        entity.addComponent(component.Drawable(kwargs['sprite'], kwargs['layer'], kwargs['offset']))

    if 'attachClass' in kwargs:
        if 'classArgs' not in kwargs:
            kwargs['classargs'] = ''
        entity.addComponent(kwargs['attachClass'](item for item in kwargs['classArgs']))
    if 'script' in kwargs:
        entity.addComponent(component.Script())
        entity.getComponent("Script").attach(kwargs['script'])

    if 'dimension' in kwargs:
        entity.addComponent(component.Dimension(kwargs['dimension']))

    return entity


class TileMap:
    def __init__(self, fileName):
        self._tmx = load_pygame(os.path.join('assets', 'levels', fileName))
        self.mapSize = (self._tmx.width, self._tmx.height)
        self.cellSize = (self._tmx.tilewidth, self._tmx.tileheight)
        self.solidityMap = [None] * self.getTileTotal()
        self.surfaces = OrderedDict()

        self.backgroundColor = pygame.Color(self._tmx.background_color) \
            if self._tmx.background_color \
            else (0, 0, 0, 0)

        for layer in self._tmx.visible_layers:
            self.parseLayer(layer)

    def parseLayer(self, layer):
        index = self._tmx.layers.index(layer)
        isSolid = layer.properties['solid'] == 'true' \
            if 'solid' in layer.properties \
            else False
        surfaceSize = (self.getWidthInPixels(), self.getHeightInPixels())
        tileSurface = pygame.Surface(surfaceSize).convert_alpha()
        tileSurface.fill(self.backgroundColor)

        for i in xrange(self.getTileTotal()):
            row = i / self.mapSize[0]
            column = i % self.mapSize[0]
            image = self._tmx.get_tile_image(column, row, index)
            if image != None:
                self.solidityMap[i] = self.solidityMap[i] or isSolid
                tileSurface.blit(image, (column * self.cellSize[0], row * self.cellSize[1]))

        self.surfaces[layer.name] = tileSurface

    def getSurfaces(self):
        return tuple(self.surfaces.values())

    def getSolidityMap(self):
        # For now, we make the solidityMap immutable
        return tuple(self.solidityMap)

    def isTileSolid(self, x, y):
        if  (0 <= x and x < self.getWidthInTiles()) and \
            (0 <= y and y < self.getHeightInTiles()):
            index = int(x + (y * self.getWidthInTiles()))
            return self.solidityMap[index] == True
        # Allow us to move one tile off screen.
        if x < -1 or x >= self.getWidthInTiles() + 1 or \
                y < -1 or y >= self.getHeightInTiles() + 1:
            return True
        else:
            return False


    def getTileTotal(self):
        return self.mapSize[0] * self.mapSize[1]

    def getWidthInPixels(self):
        return self.mapSize[0] * self.cellSize[0]

    def getHeightInPixels(self):
        return self.mapSize[1] * self.cellSize[1]

    def getWidthInTiles(self):
        return self.mapSize[0]

    def getHeightInTiles(self):
        return self.mapSize[1]

    def printSolidityMap(self):
        for y in range(self.getHeightInTiles()):
            output = []
            for x in range(self.getWidthInTiles()):
                output += [self.isTileSolid(x, y)]
            print output
