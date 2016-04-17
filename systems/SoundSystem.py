from ecs import System
import pygame

class SoundSystem(System):

    def __init__(self):
        super(SoundSystem, self).__init__();
        self.requirements = ('EventHandler',)

    def process(self, entities, dt):
    	pass

    def onAttach(self, world):
        super(SoundSystem, self).onAttach(world)
        def handle(event):
            self.eventQueue.append(event)
        world.on([pygame.USEREVENT], handle)