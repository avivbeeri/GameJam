from ecs import System
from util.enums import SOUNDEVENT
from util import Asset

class SoundSystem(System):

    def __init__(self, world, SOUND):
        super(SoundSystem, self).__init__();
        self.requirements = ('EventHandler',)
        self.SOUND = SOUND
        if self.SOUND == True:
            assetManager = Asset.Manager.getInstance()
            self.binSound = assetManager.getSound('bin.wav')
            self.hackSound = assetManager.getSound('hack.wav')
            self.leafSound = assetManager.getSound('leaves2.wav')
            self.shootSound = assetManager.getSound('shoot.wav')


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
