#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, os, pygame, random, json
import component
import auxFunctions
from collections import OrderedDict
from pygame.locals import *
from newvector import Vector2
from ecs import *
from systems import *
from pytmx.util_pygame import load_pygame
from keys import keys

with open('options.json', "r") as f:
	options = json.load(f)

inputSystem = InputSystem()
gamescreen = "menu"
worlds = OrderedDict()

# Creates a world
def setupWorld(display):
	world = World()
	groupManager = world.getManager('Group')

	city = pygame.image.load(os.path.join('assets', 'images', 'cityscape.png'))
	background = auxFunctions.create(world, position=(0,0), sprite=city, layer=-1)
	world.addEntity(background)

	mapData = auxFunctions.TileMap('test.tmx')
	for index, surface in enumerate(mapData.getSurfaces()):
		mapEntity = auxFunctions.create(world, position=(0,0), sprite=surface, layer=index)
		world.addEntity(mapEntity)

	termWin = pygame.image.load(os.path.join('assets', 'images', 'bin.png'))
	termSprite = pygame.image.load(os.path.join('assets', 'images', 'terminal.png'))
	terminal = auxFunctions.create(world, position=(16,48), dimension=(4,8), sprite=termSprite, layer=0)
	terminal.addComponent(component.Collidable())
	termState = terminal.addComponent(component.SpriteState(locked=termSprite, win=termWin))
	termState.current = 'locked'
	groupManager.add('terminal', terminal)
	world.addEntity(terminal)

	ghostSprite = pygame.image.load(os.path.join('assets', 'images', 'ghost.png'))
	playerEntity = auxFunctions.create(world, position=(8,44), sprite=ghostSprite, layer=1, dimension=(5,12))
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
		global gamescreen
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

	guardSprite = pygame.image.load(os.path.join('assets', 'images', 'guard.png'))
	guardSurprisedSprite = pygame.image.load(os.path.join('assets', 'images', 'guard_surprised.png'))
	guardAlertSprite = pygame.image.load(os.path.join('assets', 'images', 'guard_alert.png'))
	guardEntity = auxFunctions.create(world, position=(8,22), dimension=(4,14), sprite=guardSprite, layer=1)
	guardEntity.addComponent(component.Velocity((0, 0)))
	guardEntity.addComponent(component.Acceleration())
	guardEntity.addComponent(component.Radar('player'))
	guardEntity.addComponent(component.SpriteState(patrol=guardSprite, surprised=guardSurprisedSprite, alert=guardAlertSprite))
	guardState = guardEntity.addComponent(component.State())
	guardState['direction'] = 'right'
	guardState['mode'] = 'patrol'
	guardState['modeTime'] = 0

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
					worlds['level'] = setupWorld(display)
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

	liftSprite = pygame.image.load(os.path.join('assets', 'images', 'stairs.png'))
	doorEntity = auxFunctions.create(world, position=(52,44), dimension=(4,12), sprite=liftSprite, layer=0)
	doorEntity.addComponent(component.Collidable())
	groupManager.add('lift', doorEntity)
	world.addEntity(doorEntity)

	doorEntity = auxFunctions.create(world, position=(52,24), dimension=(4,12), sprite=liftSprite, layer=0)
	doorEntity.addComponent(component.Collidable())
	groupManager.add('lift', doorEntity)
	world.addEntity(doorEntity)

	doorEntity = auxFunctions.create(world, position=(28,4), dimension=(4,12), sprite=liftSprite, layer=0)
	doorEntity.addComponent(component.Collidable())
	groupManager.add('lift', doorEntity)
	world.addEntity(doorEntity)

	doorEntity = auxFunctions.create(world, position=(28,24), dimension=(4,12), sprite=liftSprite, layer=0)
	doorEntity.addComponent(component.Collidable())
	groupManager.add('lift', doorEntity)
	world.addEntity(doorEntity)

	binSprite = pygame.image.load(os.path.join('assets', 'images', 'plant.png'))
	binFullSprite = pygame.image.load(os.path.join('assets', 'images', 'plant_hiding.png'))
	binEntity = auxFunctions.create(world, position=(38,24), dimension=(10,12), sprite=binSprite, layer=0)
	binEntity.addComponent(component.Collidable())
	binState = binEntity.addComponent(component.SpriteState(empty=binSprite, occupied=binFullSprite))
	groupManager.add('hidable', binEntity)
	world.addEntity(binEntity)

	world.addSystem(inputSystem)
	world.addSystem(RadarSystem())
	world.addSystem(ScriptSystem())
	world.addSystem(PhysicsSystem())
	world.addSystem(TileCollisionSystem(mapData))
	world.addSystem(RenderSystem(display))
	world.addSystem(SpriteSystem())
	return world

def optionsMenu(display):
	world = World()
	### NOTE: DON'T ADD ENTITES YET! ###
	# See setupMenu for the comments on this :)
	menuImage = pygame.image.load(os.path.join('assets', 'images', 'cityscape.png'))
	background = auxFunctions.create(world, position=(0,0), sprite=menuImage, layer=-2)
	world.addEntity(background)

	menuText = pygame.image.load(os.path.join('assets', 'images', 'options.png'))
	text = auxFunctions.create(world, position=(0,0), sprite=menuText, layer=-1)
	world.addEntity(text)

	onImage = pygame.image.load(os.path.join("assets", "images", "on.png"))
	musicOn = auxFunctions.create(world, position=(53,22), sprite=onImage, layer=3)
	soundOn = auxFunctions.create(world, position=(53,34), sprite=onImage, layer=3)
	if options["MUSIC"] == False:
		musicOn.getComponent("Drawable").layer = -3
	if options["SOUND"] == False:
		soundOn.getComponent("Drawable").layer = -3
	world.addEntity(musicOn)
	world.addEntity(soundOn)
	### FEEL FREE TO ADD ENTITIES AGAIN ###

	cursorImage = pygame.image.load(os.path.join('assets', 'images', 'cursor.png'))
	cursor = auxFunctions.create(world, position=(2,18), sprite=cursorImage, layer=3)

	cursorEventHandler = cursor.addComponent(component.EventHandler())
	def move(entity, event):
		global gamescreen, options
		currentPosition = entity.getComponent("Position")
		if event.key in keys.keys():
			if keys[event.key] == "Up":
				if currentPosition.value[1] > 18:
					currentPosition.value += Vector2(0, -12)
			elif keys[event.key] == "Down":
				if currentPosition.value[1] < 30:
					currentPosition.value += Vector2(0, 12)
			elif keys[event.key] in ("Interact", "Enter"):
				if currentPosition.value[1] == 18:
					options["MUSIC"] = not options["MUSIC"]
					worlds[gamescreen].getEntity(2).getComponent("Drawable").layer = 0 - \
							worlds[gamescreen].getEntity(2).getComponent("Drawable").layer
					# This swaps the value between 3 and -3 - IE visible or not.
					if options["MUSIC"] == True:
						pygame.mixer.music.play(loops=-1)
					else:
						pygame.mixer.music.stop()
				elif currentPosition.value[1] == 30:
					options["SOUND"] = not options["SOUND"]
					worlds[gamescreen].getEntity(3).getComponent("Drawable").layer = 0 - \
							worlds[gamescreen].getEntity(3).getComponent("Drawable").layer
				else:
					pass
			with open('options.json', "w") as f:
				json.dump(options, f, indent=4)
	cursorEventHandler.attachHandler(pygame.KEYDOWN, move)
	world.addEntity(cursor)

	world.addSystem(RenderSystem(display))
	world.addSystem(inputSystem)
	return world

def setupMenu(display):
	world = World()

	# Add the music
	pygame.mixer.music.load(os.path.join('assets','music','BlueBeat.wav'))
	if options["MUSIC"] == True:
		pygame.mixer.music.play(loops=-1)

	# Add the background image
	menuImage = pygame.image.load(os.path.join('assets', 'images', 'cityscape.png'))
	background = auxFunctions.create(world, position=(0,0), sprite=menuImage, layer=-2)
	world.addEntity(background)

	# The text that goes on top of the world is here.
	menuText = pygame.image.load(os.path.join('assets', 'images', 'menu.png'))
	text = auxFunctions.create(world, position=(0,0), sprite=menuText, layer=-1)
	world.addEntity(text)

	# Add the movable component
	cursorImage = pygame.image.load(os.path.join('assets', 'images', 'cursor.png'))
	cursor = auxFunctions.create(world, position=(2,22), lastPosition=(2,22), sprite=cursorImage, layer=0)
	# Which can move (a bit).
	cursorEventHandler = cursor.addComponent(component.EventHandler())
	def move(entity, event):
		global gamescreen
		currentPosition = entity.getComponent("Position")
		if event.key in keys.keys():
			if keys[event.key] == "Up":
				if currentPosition.value[1] > 22:
					currentPosition.value += Vector2(0, -13)
			elif keys[event.key] == "Down":
				if currentPosition.value[1] < 48:
					currentPosition.value += Vector2(0, 13)
			elif keys[event.key] in ("Interact", "Enter"):
				if currentPosition.value == Vector2(2,22):
					worlds["level"] = setupWorld(display)
					gamescreen = "level"
				elif currentPosition.value == Vector2(2,35):
					worlds["options"] = optionsMenu(display)
					gamescreen = "options"
				elif currentPosition.value == Vector2(2,48):
					quit()
				else:
					pass
			elif keys[event.key] == "Exit":
				quit()
	cursorEventHandler.attachHandler(pygame.KEYDOWN, move)
	world.addEntity(cursor)

	world.addSystem(RenderSystem(display))
	world.addSystem(inputSystem)
	return world

def quitcheck(eventQueue):
	retval = 0
	global gamescreen
	for event in eventQueue:
	# Check if the user has quit, and if so quit.
		if event.type == QUIT:
			retval = 1
		elif event.type == KEYDOWN:
			if event.key in keys.keys():
				if keys[event.key] == "Exit":
					worlds.popitem()
					gamescreen = worlds.keys()[-1]
		elif (event.type == USEREVENT) and (event.code == "TIMERQUIT"):
			gamescreen = "level"
	eventQueue = []
	return retval


def main():
	global gamescreen, worlds
	pygame.init()

	outputSize = (options["SIZE"], options["SIZE"])
	#Create the window and caption etc.
	display = pygame.display.set_mode(outputSize)
	pygame.display.set_caption('Ghost')
	pygame.mouse.set_visible(0)

	# Create and initialise drawable canvas
	screen = pygame.Surface((64, 64), pygame.SRCALPHA)
	screen.fill((0,0,0))
	screen = screen.convert_alpha()

	# Initalise the game loop clock
	clock = pygame.time.Clock()

	# Create the world
	# Later this could be delegated to a "State" object.
	worlds["menu"] = setupMenu(screen)
	renderSystem = RenderSystem(screen)
	eventQueue = []

	dt = (1.0 / 60.0) * 1000;
	accumulator = 0
	currentTime = pygame.time.get_ticks()

	while quitcheck(eventQueue) != 1:
		newTime = pygame.time.get_ticks()
		frameTime = newTime - currentTime
		currentTime = newTime
		accumulator += frameTime

		# Retrieve input events for processing
		eventQueue = pygame.event.get()
		inputSystem.eventQueue += eventQueue
		while (accumulator >= dt):
			worlds[gamescreen].update(dt / 1000.0)
			accumulator -= dt

		# We do rendering outside the regular update loop for performance reasons
		# See: http://gafferongames.com/game-physics/fix-your-timestep/
		entities = renderSystem.getProcessableEntities(worlds[gamescreen])
		renderSystem.process(entities, 0)
		display.blit(pygame.transform.scale(screen, outputSize), (0, 0))
		pygame.display.flip()

if __name__ == '__main__': main()
