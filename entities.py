import auxFunctions
import component
import pygame, os
from keys import keys
from newvector import Vector2

# Load assets
# Stairs
stairSprite = pygame.image.load(os.path.join('assets', 'images', 'stairs.png'))

# Plants
plantSprite = pygame.image.load(os.path.join('assets', 'images', 'plant.png'))
plantHidingSprite = pygame.image.load(os.path.join('assets', 'images', 'plant_hiding.png'))

# Bins
binSprite = pygame.image.load(os.path.join('assets', 'images', 'bin.png'))
binFullSprite = pygame.image.load(os.path.join('assets', 'images', 'bin_full.png'))

# Guards
guardSprite = pygame.image.load(os.path.join('assets', 'images', 'guard.png'))
guardSurprisedSprite = pygame.image.load(os.path.join('assets', 'images', 'guard_surprised.png'))
guardAlertSprite = pygame.image.load(os.path.join('assets', 'images', 'guard_alert.png'))

# Terminal
termWin = pygame.image.load(os.path.join('assets', 'images', 'terminalwin.png'))
termSprite = pygame.image.load(os.path.join('assets', 'images', 'terminal.png'))

# Text
pygame.font.init()
pressStart = pygame.font.Font(os.path.join('assets', 'fonts', 'visitor1.ttf'), 10)

ghostSprite = pygame.image.load(os.path.join('assets', 'images', 'ghost.png'))
def createGhost(world, position):
    groupManager = world.getManager('Group')
    playerEntity = auxFunctions.create(world, position=position, sprite=ghostSprite, layer=1, dimension=(5,12))
    playerEntity.addComponent(component.Velocity((0, 0)))
    playerEntity.addComponent(component.Acceleration())
    playerEntity.addComponent(component.Visible())
    playerState = playerEntity.addComponent(component.State())
    playerState['flipped'] = False
    playerState['hiding'] = False
    playerEntity.addComponent(component.Collidable())
    playerEntity.addComponent(component.TargetVelocity())

    # Demonstration of how to handle input.
    def handleInput(entity, event):
        targetVelocityComponent = entity.getComponent('TargetVelocity')
        velocityComponent = entity.getComponent('Velocity')
        playerState = entity.getComponent('State')
        if event.type == pygame.KEYDOWN:
            if event.key in keys.keys():
                if keys[event.key] == "Left":
                    playerState['flipped'] = True
                    targetVelocityComponent.value += Vector2(-0.5, 0)
                elif keys[event.key] == "Right":
                    playerState['flipped'] = False
                    targetVelocityComponent.value += Vector2(0.5, 0)
                elif keys[event.key] == "Interact":
                    collisionSystem = world.getSystem('TileCollisionSystem')
                    collisions = collisionSystem.getEntityCollisions(entity.id)
                    for other in collisions:
                        if groupManager.check(other, 'terminal'):
                            other.getComponent('SpriteState').current = "win"
                        elif groupManager.check(other, 'lift'):
                            originalLiftId = other.id
                            liftPosition = other.getComponent('Position').value
                            liftTilePosition = collisionSystem.getTilePosition(liftPosition)
                            for height in range(collisionSystem.tileMap.mapSize[1]):
                                entities = collisionSystem.getEntitiesInTile(liftTilePosition.x, height)
                                for other in entities:
                                    if groupManager.check(other, 'lift') and \
                                            other.id != originalLiftId:
                                        newPosition = entity.getComponent('Position').value
                                        liftPosition = other.getComponent('Position').value
                                        newPosition.y = liftPosition.y
                                        return
                        elif groupManager.check(other, 'hidable'):
                            playerState['hiding'] = True
                            entity.removeComponent('Visible')
                            entity.removeComponent('Drawable')
                            entity.removeComponent('Collidable')
                            other.getComponent('SpriteState').current = 'occupied'
                            playerState['cover'] = other
                if not playerState['hiding']:
                    entity.getComponent('Drawable').flip(playerState['flipped'])
        elif event.type == pygame.KEYUP:
            if event.key in keys.keys():
                if keys[event.key] == "Left":
                    targetVelocityComponent.value += Vector2(+0.5, 0)
                elif keys[event.key] == "Right":
                    targetVelocityComponent.value += Vector2(-0.5, 0)
                elif keys[event.key] == "Interact":
                    if playerState['hiding']:
                        playerState['hiding'] = False
                        other = playerState['cover']
                        playerState['cover'] = None
                        entity.addComponent(component.Visible())
                        entity.addComponent(component.Drawable(ghostSprite, 1))
                        entity.addComponent(component.Collidable())
                        other.getComponent('SpriteState').current = 'empty'

        velocityComponent.value = targetVelocityComponent.value

    playerInputHandler = playerEntity.addComponent(component.EventHandler())
    playerInputHandler.attachHandler(pygame.KEYDOWN, handleInput)
    playerInputHandler.attachHandler(pygame.KEYUP, handleInput)
    groupManager.add('player', playerEntity)
    world.addEntity(playerEntity)

def createBin(world, position):
    groupManager = world.getManager('Group')
    binEntity = auxFunctions.create(world, position=position, dimension=(10,12), sprite=binSprite, layer=0)
    binEntity.addComponent(component.Collidable())
    binState = binEntity.addComponent(component.SpriteState(empty=binSprite, occupied=binFullSprite))
    groupManager.add('hidable', binEntity)
    world.addEntity(binEntity)

def createPlant(world, position):
    groupManager = world.getManager('Group')
    binEntity = auxFunctions.create(world, position=position, dimension=(10,12), sprite=binSprite, layer=0)
    binEntity.addComponent(component.Collidable())
    binState = binEntity.addComponent(component.SpriteState(empty=plantSprite, occupied=plantHidingSprite))
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

def createTerminal(world, position):
    groupManager = world.getManager('Group')
    terminal = auxFunctions.create(world, position=position, dimension=(4,8), sprite=termSprite, layer=0)
    terminal.addComponent(component.Collidable())
    termState = terminal.addComponent(component.SpriteState(locked=termSprite, win=termWin))
    termState.current = 'locked'
    groupManager.add('terminal', terminal)
    world.addEntity(terminal)

def createText(world, position, text):
    renderedText = pressStart.render(text, False, (255,255,255))
    blittedText = auxFunctions.create(world, position=position, sprite=renderedText, layer=6)
    world.addEntity(blittedText)