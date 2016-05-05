from pygame import Surface, Rect

class Sprite(object):

    def __init__(self, surface, totalFrames=1, frameRate=0, frameDimensions=(1,1), spriteDimensions=None, loop=True):
        if spriteDimensions is None:
            spriteDimensions = spritesheet.get_size()
        self.frames = getFramesFromSpriteSheet(spritesheet, totalFrames, frameDimensions, spriteDimensions)
        self.totalFrames = totalFrames
        self.currentFrame = 0
        self.frameRate = frameRate
        self.loop = loop

    def getCurrentFrame(self):
        return self.frames[self.currentFrame]

    def nextFrame(self):
        self.currentFrame += 1
        if self.loop:
            self.currentFrame %= self.totalFrames


def getFramesFromSpriteSheet(spritesheet, frameDimensions, spriteDimensions, totalFrames):
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
        surface = Surface((spriteWidth, spriteHeight))
        surface.blit(spritesheet, (0, 0), rect)
        frames.append(surface)
    return frames
