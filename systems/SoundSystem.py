from ecs import System
import pygame

pygame.mixer.init()

class SoundSystem(System):

    def __init__(self):
        super(SoundSystem, self).__init__();
        self.requirements = ('EventHandler',)
        world.on([pygame.USEREVENT], handle)
        self.binSound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'bin.wav'))
        self.hackSound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'hack.wav'))
        self.leafSound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'leaves2.wav'))
        self.shootSound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'shoot.wav'))

    def process(self, event):
        if event.code == "bin":
            self.binSound.play()
        elif event.code == 'terminal':
            self.hackSound.play()
        elif event.code == 'plant':
            self.leafSound.play()
        elif event.code == 'shoot':
            self.shootSound.play()
        else:
            print "Event code not known!"

    def onAttach(self, world):
        super(SoundSystem, self).onAttach(world)
        def handle(event):
            self.eventQueue.append(event)