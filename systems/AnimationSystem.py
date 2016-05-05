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

            # Advance the animation
            animation.accumulator += dt
            if animation.accumulator > (1.0 / animation.framerate):
                animation.accumulator -= (1.0 / animation.framerate)
                drawable.image.nextFrame()
