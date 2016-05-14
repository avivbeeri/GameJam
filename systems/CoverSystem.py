import pygame
from ecs import System
from util import enums
from util import Asset
import component

class CoverSystem(System):

    def __init__(self):
        super(CoverSystem, self).__init__();
        self.requirements = ('Cover', 'Interactable')

    def process(self, entities, dt):
        # process the queued events
        for event in self.eventQueue:
            for entity in entities:
                cover = entity.getComponent('Cover')
                spriteState = entity.getComponent('SpriteState')

                if event.type == enums.INTERACT and entity.id == event.target:
                    playerEntity = self.world.getEntity(event.entity)
                    player = playerEntity.getComponent('PlayerInput')
                    cover.occupant = event.entity

                    # Assume 'other' is always a player entity
                    player.enabled = False
                    playerEntity.removeComponent('Drawable')
                    playerEntity.removeComponent('Visible')
                    playerEntity.removeComponent('Collidable')
                    spriteState.current = 'occupied'

                    groupManager = self.world.getManager('Group')
                    if groupManager.check(entity, 'plant'):
                        self.world.post(pygame.event.Event(enums.SOUNDEVENT, code='plant'))
                    elif groupManager.check(entity, 'bin'):
                        self.world.post(pygame.event.Event(enums.SOUNDEVENT, code='bin'))
                elif event.type == enums.STOPINTERACT and cover.occupant == event.target:
                    # Assume 'other' is always a player entity
                    playerEntity = self.world.getEntity(event.target)
                    player = playerEntity.getComponent('PlayerInput')
                    player.enabled = True
                    cover.occupant = None
                    ghostIdleSprite = Asset.Manager.getInstance().getSprite('ghost.png')
                    playerEntity.addComponent(component.Drawable(ghostIdleSprite, 1))
                    playerEntity.addComponent(component.Collidable())
                    playerEntity.addComponent(component.Visible())
                    '''
                    Enabling this line locks Ghost to reappear at the position of the cover.
                    If the cover is poorly placed, this will cause collision issues.
                    playerEntity.getComponent('Position').value.x = entity.getComponent('Position').value.x
                    '''
                    spriteState.current = 'empty'
        del self.eventQueue[:]

    def onAttach(self, world):
        super(CoverSystem, self).onAttach(world)
        def handle(event):
            self.eventQueue.append(event)
        world.on([enums.INTERACT, enums.STOPINTERACT], handle)
