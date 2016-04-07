from pytmx.util_pygame import load_pygame

import pygame
import os

class TileMap:

    def __init__(self, fileName):
        self.mapLayer = {}
        self.surfaces = {}
        self.tmx = load_pygame(os.path.join('assets', fileName))
        self.mapSize = (self.tmx.width, self.tmx.height)
        self.properties = self.tmx.properties
        self.cellSize = (self.tmx.tilewidth, self.tmx.tileheight)

        self.backgroundColor = pygame.Color(self.tmx.background_color) \
            if self.tmx.background_color \
            else (0, 0, 0, 0)


    def getLayerSurface(self, layer):
        if not layer in self.surfaces:
            mapSize = self.mapSize
            cellSize = self.cellSize
            surfaceSize = ((mapSize[0] * cellSize[0]), (mapSize[1] * cellSize[1]))

            tileSurface = pygame.Surface(surfaceSize).convert_alpha()
            tileSurface.fill(self.backgroundColor)
            # Calculate the total number of tiles
            tileTotal = mapSize[0] * mapSize[1]
            # Initialise the tileMap.
            self.mapLayer[layer] = [None] * tileTotal
            tileData = self.mapLayer[layer]

            for i in xrange(tileTotal):
                row = i / mapSize[0]
                column = i % mapSize[1]

                image = self.tmx.get_tile_image(column, row, layer)
                if image != None:
                    tileData[i] = 'SOLID'
                    tileSurface.blit(image, (column * cellSize[0], row * cellSize[1]))
        else:
            tileSurface = self.surfaces[layer]

        return tileSurface

    def getTileData(self, x, y, layer):
        if x > self.mapSize[0] or y > self.mapSize[1]:
            raise ValueError('Position is outside of tilemap')
        if not layer in self.mapLayer:
            raise ValueError('Layer does not exist or has not been initialised')

        index = int(y * self.mapSize[0] + x)
        return self.mapLayer[layer][index]
