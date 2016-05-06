from pygame import Surface, Rect, locals, image
from .resourcepath import resource_path
from os import path
from weakref import WeakValueDictionary

class Manager(object):
    INSTANCE = None
    def __init__(self):
        self.map = {}# WeakValueDictionary()

    def get(self, key):
        if key not in self.map:
            surface = Manager.loadImage(key)
            # TODO: Look up sprite animation info from somewhere.
            # We assume that we re only loading static from here for now
            spriteInfo = SpriteData(surface)
            self.map[key] = spriteInfo
        return Sprite(self.map[key])

    def put(self, key, value):
        self.map[key] = value
        return value

    @staticmethod
    def getInstance():
        if not Manager.INSTANCE:
            Manager.INSTANCE = Manager()
        return Manager.INSTANCE

    @staticmethod
    def loadImage(filename):
        return image.load(resource_path(path.join('assets', 'images', filename)))


class SpriteData(object):
    def __init__(self, surface, totalFrames=1, frameDimensions=(1,1), spriteDimensions=None):
        if spriteDimensions is None:
            spriteDimensions = surface.get_size()
        self.frames = getFramesFromSpriteSheet(surface, totalFrames, frameDimensions, spriteDimensions)
        self.totalFrames = totalFrames
        self.lastFrame = self.totalFrames - 1

    def getKeyframe(self, frame):
        return self.frames[frame]

class Sprite(object):
    def __init__(self, spriteData, loop=True, currentFrame=0):
        if isinstance(spriteData, SpriteData):
            self.spriteData = spriteData
        else:
            self.spriteData = SpriteData(spriteData)
        self.loop = loop
        self.currentFrame = currentFrame

    def current(self):
        return self.spriteData.getKeyframe(self.currentFrame)

    def next(self):
        self.currentFrame += 1
        if self.loop:
            self.currentFrame %= self.spriteData.totalFrames
        self.currentFrame = min(self.currentFrame, self.spriteData.lastFrame)

def getFramesFromSpriteSheet(spritesheet, totalFrames, frameDimensions, spriteDimensions):
    frames = []
    frameCols, frameRows = frameDimensions
    if totalFrames < 1 or frameCols < 1 or frameRows < 1:
        raise ValueError('Invalid frame dimensions')

    spriteWidth, spriteHeight = spriteDimensions
    for currentFrame in range(totalFrames):
        row = currentFrame / frameCols
        column = currentFrame % frameCols
        if row > frameRows or column > frameCols:
            raise ValueError('Too many rows!')
        rect = Rect(column * spriteWidth, row * spriteHeight, spriteWidth, spriteHeight)
        surface = Surface((spriteWidth, spriteHeight), locals.SRCALPHA)
        surface.blit(spritesheet, (0, 0), rect)
        frames.append(surface)
    return frames
