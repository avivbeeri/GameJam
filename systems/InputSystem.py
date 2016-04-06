import pygame
from ecs import System

class InputSystem(System):

    def __init__(self):
        super(InputSystem, self).__init__();
        self.requirements = ('EventHandler',)
        self.eventQueue = []

    def process(self, entities, dt):
        # process the queued events
        for event in self.eventQueue:
            for entity in entities:
                inputComponent = entity.getComponent('EventHandler')
                inputComponent.handle(event)
        self.eventQueue = []
