import pygame
from ecs import System

class SpriteSystem(System):

    def __init__(self):
        super(SpriteSystem, self).__init__()
        self.requirements = ('Drawable', 'SpriteState')

    def process(self, entities, dt):
        for entity in entities:
            currentSprite = entity.getComponent("Drawable")
            possibleStates = entity.getComponent("SpriteState")
            currentState = entity.getComponent("SpriteState").current
            if currentState is not None:
                currentSprite.set(possibleStates[currentState])
