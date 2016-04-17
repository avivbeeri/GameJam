from ecs import System
from util.enums import SOUNDEVENT
import pygame, os

pygame.mixer.init()

class SoundSystem(System):

    def __init__(self, world, SOUND):
        super(SoundSystem, self).__init__();
        self.requirements = ('EventHandler',)
        self.binSound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'bin.wav'))
        self.hackSound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'hack.wav'))
        self.leafSound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'leaves2.wav'))
        self.shootSound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'shoot.wav'))
        self.SOUND = SOUND

    def process(self, entities, dt):
        if self.SOUND == True:
            for event in self.eventQueue:
                if event.code == "bin":
                    self.binSound.play(0)
                elif event.code == 'terminal':
                    self.hackSound.play(0)
                elif event.code == 'plant':
                    self.leafSound.play(0)
                elif event.code == 'shoot':
                    self.shootSound.play(0)
                else:
                    print "Event code not known!"
        del self.eventQueue[:]

    def onAttach(self, world):
        super(SoundSystem, self).onAttach(world)
        def handle(event):
            self.eventQueue.append(event)
        world.on([SOUNDEVENT], handle)