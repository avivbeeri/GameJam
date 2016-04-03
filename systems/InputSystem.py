import pygame
from pygame import key
from ecs import System

class InputSystem(System):

    def __init__(self):
        super(InputSystem, self).__init__();
        self.requirements = ('Input',)

    def process(self, entities):
        # check for input
        keys = key.get_pressed()
        for entity in entities:
            inputComponent = entity.getComponent('Input')
            inputComponent.process(keys)
