import pygame
from ecs import System
from util import enums

class InteractionSystem(System):

    def __init__(self):
        super(InteractionSystem, self).__init__();
        self.requirements = ('Interactable',)

    def process(self, entities, dt):
        # process the queued events
        for event in self.eventQueue:
            for entity in entities:
                if entity.id == event.target:
                    entity.getComponent('Interactable').handle(event)
        del self.eventQueue[:]

    def onAttach(self, world):
        super(InteractionSystem, self).onAttach(world)
        def handle(event):
            self.eventQueue.append(event)
        world.on([enums.INTERACT], handle)
