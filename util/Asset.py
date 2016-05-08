from pygame import Surface, Rect, locals, image, mixer, font
from .resourcepath import resource_path
from os import path

font.init()
class Manager(object):
    INSTANCE = None
    def __init__(self):
        '''
        Ideally we would use a WeakValueDictionary here so that garbage collection
        will clear memory when a Sprite is no longer being referenced, but this causes
        problems when we have to manually build Animation SpriteData currently.
        '''
        self.map = {}

    def get(self, key):
        return self.map.get(key)

    def getAllSprites(self, keys):
        values = []
        for key in keys:
            values.append(self.getSprite(key))
        return values

    def put(self, key, value):
        self.map[key] = value
        return value

    def getFont(self, key, size=8):
        if (key, size) not in self.map:
            self.put((key, size), Manager.loadFont(key, size))
        return self.get((key, size))

    def getSound(self, key):
        if key not in self.map:
            self.put(key, Manager.loadSound(key))
        return self.get(key)

    def getSprite(self, key):
        value = self.get(key)
        if value is None:
            surface = Manager.loadImage(key)
            # TODO: Look up sprite animation info from somewhere.
            # We assume that we re only loading static from here for now
            spriteInfo = SpriteData(surface)
            return self.putSprite(key, spriteInfo)
        else:
            return Sprite(value)

    def putSprite(self, key, value):
        self.map[key] = value
        return Sprite(value)

    def unload(self, key):
        value = self.map[key]
        self.map[key] = None
        return value

    @staticmethod
    def getInstance():
        if not Manager.INSTANCE:
            Manager.INSTANCE = Manager()
        return Manager.INSTANCE

    @staticmethod
    def loadImage(filename):
        return image.load(resource_path(path.join('assets', 'images', filename)))

    @staticmethod
    def loadSound(filename):
        return mixer.Sound(resource_path(path.join('assets', 'sounds', filename)))

    @staticmethod
    def loadFont(filename, size):
        return font.Font(resource_path(path.join('assets', 'fonts', filename)), size)


class SpriteData(object):
    def __init__(self, surface, totalFrames=1, frameDimensions=(1,1), spriteDimensions=None):
        if isinstance(surface, Surface):
            self.frames = SpriteData.getFramesFromSpriteSheet(surface, totalFrames, frameDimensions, spriteDimensions)
            self.totalFrames = totalFrames
        else:
            self.frames = surface
            self.totalFrames = len(self.frames)
        self.lastFrame = self.totalFrames - 1


    def getKeyframe(self, frame):
        return self.frames[frame]

    @staticmethod
    def getFramesFromSpriteSheet(spritesheet, totalFrames, frameDimensions, spriteDimensions):
        if spriteDimensions is None:
            spriteDimensions = spritesheet.get_size()

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
