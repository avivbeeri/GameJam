import pygame
from ecs import System
from util import enums
from util.enums import keys
from newvector import Vector2

class PlayerInputSystem(System):

    def __init__(self):
        super(PlayerInputSystem, self).__init__()
        self.requirements = ('PlayerInput', 'Velocity')

    def process(self, entities, dt):
        for entity in entities:
            velocityComponent = entity.getComponent("Velocity")
            player = entity.getComponent("PlayerInput")
            playerSpriteState = entity.getComponent('SpriteState')
            targetVelocity = Vector2(velocityComponent.value)
            if player.enabled:
                for event in self.eventQueue:
                    if event.type == pygame.KEYDOWN:
                        if event.key in keys:
                            if keys[event.key] == "Left":
                                targetVelocity += Vector2(-0.5, 0)
                            elif keys[event.key] == "Right":
                                targetVelocity += Vector2(0.5, 0)
                            elif keys[event.key] == ("Interact") and player.enabled:
                                collisions = entity.getComponent('Collidable').collisionSet
                                for other in collisions:
                                    if other.hasComponent('Interactable'):
                                        event = pygame.event.Event(enums.INTERACT, { 'target': other.id, 'entity': entity.id })
                                        self.world.post(event)
                    elif event.type == pygame.KEYUP and velocityComponent.value.length() != 0:
                        if event.key in keys:
                            if keys[event.key] == "Left":
                                targetVelocity -= Vector2(-0.5, 0)
                            elif keys[event.key] == "Right":
                                targetVelocity -= Vector2(0.5, 0)
                playerSpriteState.current = 'moving' if targetVelocity.length() != 0 else 'idle'
            else:
                targetVelocity = Vector2()
            velocityComponent.value = targetVelocity
        del self.eventQueue[:]

    def onAttach(self, world):
        super(PlayerInputSystem, self).onAttach(world)
        def handle(event):
            self.eventQueue.append(event)
        world.on([pygame.KEYUP, pygame.KEYDOWN], handle)
