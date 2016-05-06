import pygame
from ecs import System
from util import Asset

class SpriteSystem(System):

    def __init__(self):
        super(SpriteSystem, self).__init__()
        self.requirements = ('Drawable', 'SpriteState')

    def process(self, entities, dt):
        for entity in entities:
            currentSprite = entity.getComponent("Drawable")
            possibleStates = entity.getComponent("SpriteState")
            currentState = possibleStates.current
            lastState = possibleStates.last
            if currentState is not None and currentState is not lastState:
                newSprite = Asset.Manager.getInstance().get(possibleStates[currentState])
                currentSprite.set(newSprite)
                possibleStates.last = currentState
