import pygame
from ecs import System

class AnimationSystem(System):

    def __init__(self):
        super(AnimationSystem, self).__init__()
        self.requirements = ('Drawable', 'Animation')

    def process(self, entities, dt):
        for entity in entities:
            drawable = entity.getComponent("Drawable")
            animation = entity.getComponent("Animation")
            # TODO: Get full surface and store it

            # Advance the animation
            animation.accumulator += dt
            if animation.accumulator > (1.0 / animation.framerate):
                animation.accumulator = 0
                row = animation.currentFrame / animation.frameCols
                column = animation.currentFrame % animation.frameCols

                height = animation.spriteHeight
                width = animation.spriteWidth
                rect = pygame.Rect(column * width, row * height, width, height)
                drawable.selectArea(rect)
                animation.currentFrame = (animation.currentFrame + 1) % animation.totalFrames
