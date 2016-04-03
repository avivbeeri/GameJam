import pygame
from ecs import System

class InputSystem(System):

    def __init__(self):
        super(InputSystem, self).__init__();
        self.requirements = ('EventHandler',)
        self.eventQueue = []

    def process(self, entities):
        # check for input
        # keys = pygame.key.get_pressed()
        for event in self.eventQueue:
            for entity in entities:
                inputComponent = entity.getComponent('EventHandler')
                inputComponent.handle(event)
