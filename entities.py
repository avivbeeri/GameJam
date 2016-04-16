import auxFunctions
import component
import pygame, os

# Load assets
# Stairs
stairSprite = pygame.image.load(os.path.join('assets', 'images', 'stairs.png'))

# Plants
binSprite = pygame.image.load(os.path.join('assets', 'images', 'plant.png'))
binFullSprite = pygame.image.load(os.path.join('assets', 'images', 'plant_hiding.png'))

# Guards
guardSprite = pygame.image.load(os.path.join('assets', 'images', 'guard.png'))
guardSurprisedSprite = pygame.image.load(os.path.join('assets', 'images', 'guard_surprised.png'))
guardAlertSprite = pygame.image.load(os.path.join('assets', 'images', 'guard_alert.png'))

def createPlant(world, position):
    groupManager = world.getManager('Group')
    binEntity = auxFunctions.create(world, position=position, dimension=(10,12), sprite=binSprite, layer=0)
    binEntity.addComponent(component.Collidable())
    binState = binEntity.addComponent(component.SpriteState(empty=binSprite, occupied=binFullSprite))
    groupManager.add('hidable', binEntity)
    world.addEntity(binEntity)

def createStairs(world, position):
    groupManager = world.getManager('Group')
    stairEntity = auxFunctions.create(world, position=position, dimension=(5,12), sprite=stairSprite, layer=0, offset=(0,-1))
    stairEntity.addComponent(component.Collidable())
    groupManager.add('lift', stairEntity)
    world.addEntity(stairEntity)


def createGuard(world, position, accOffset=0):
    groupManager = world.getManager('Group')
    guardEntity = auxFunctions.create(world, position=position, dimension=(4,14), sprite=guardSprite, layer=1)
    guardEntity.addComponent(component.Velocity((0, 0)))
    guardEntity.addComponent(component.Acceleration())
    guardEntity.addComponent(component.Radar('player'))
    guardEntity.addComponent(component.SpriteState(patrol=guardSprite, surprised=guardSurprisedSprite, alert=guardAlertSprite))
    guardState = guardEntity.addComponent(component.State())
    guardState['direction'] = 'right'
    guardState['mode'] = 'patrol'
    guardState['modeTime'] = accOffset


    def guardScript(entity, dt):
        global worlds
        radar = entity.getComponent('Radar')
        state = entity.getComponent('State')
        spriteState = entity.getComponent('SpriteState')
        drawable = entity.getComponent('Drawable')

        def isVisible(entity, radar):
            if 'player' not in radar.targets or len(radar.targets['player']) == 0:
                return False

            playerPing = next(iter(radar.targets['player']))
            player = playerPing.entity

            entityPosition  = entity.getComponent('Position').value
            entityDirection = entity.getComponent('State')['direction']
            playerPosition  = player.getComponent('Position').value
            collisionSystem = world.getSystem('TileCollisionSystem')
            if (entityDirection == 'right' and entityPosition.x <= playerPosition.x) or \
                    (entityDirection == 'left' and entityPosition.x > playerPosition.x) :
                return playerPing.visible
            else:
                return False

        def getPlayerDirection(radar):
            playerPing = next(iter(radar.targets['player']))
            player = playerPing.entity
            return playerPing.distance.normalize() * 0.3

        def shouldImageFlip():
            return state['direction'] == 'left'


        state['modeTime'] += dt
        if state['mode'] == 'patrol':
            if state['modeTime'] > 5:
                state['modeTime'] = 0
                state['direction'] = 'left' if state['direction'] == 'right' else 'right'

            if isVisible(entity, radar):
                state['mode'] = 'surprised'
                state['modeTime'] = 0
        elif state['mode'] == 'surprised':
            if state['modeTime'] > 0.6:
                if isVisible(entity, radar):
                    state['mode'] = 'alert'
                    state['modeTime'] = 0
                else:
                    state['mode'] = 'patrol'
        elif state['mode'] == 'alert':
            if isVisible(entity, radar):
                if state['modeTime'] > 0.4:
                    print 'FIRE EVENT: GAMEOVER'
                    quit()
            else:
                state['mode'] = 'surprised'
                drawable.flip(shouldImageFlip())
                state['modeTime'] = 0
        elif state['mode'] == 'chase':
            # We aren't currently using this, but it is useful!
            velocity = entity.getComponent('Velocity')
            if isVisible(entity, radar):
                velocity.value = getPlayerDirection(radar)
            else:
                velocity.value = Vector2()
                state['mode'] = 'patrol'

        drawable.flip(shouldImageFlip())
        spriteState.current = state['mode']


    scriptComponent = guardEntity.addComponent(component.Script())
    scriptComponent.attach(guardScript)
    collidable = guardEntity.addComponent(component.Collidable())
    world.addEntity(guardEntity)
