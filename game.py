#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, os, pygame, random
import component
import maze
import tileMap
from collections import OrderedDict
from pygame.locals import *
from pygame.math import Vector2
from ecs import *
from systems import RenderSystem, PhysicsSystem, InputSystem, ScriptSystem, TileCollisionSystem
from pytmx.util_pygame import load_pygame
from options import *

inputSystem = InputSystem()
gamescreen = "menu"
worlds = OrderedDict()

def setupMaze(display, (time, cellSize)):
	world = World()

	# Creating the frame that goes around the maze.
	frame = world.createEntity()
	frame.addComponent(component.Position((0,0)))
	mazeFrame = pygame.image.load(os.path.join('assets', 'images', 'puzzleframe.png'))
	mazeFrame.convert()
	frame.addComponent(component.Drawable(mazeFrame, 1))
	world.addEntity(frame)

	# Creating the object for the timer.
	timer = world.createEntity()
	timer.addComponent(component.Position((4,display.get_height()-3)))
	timeLayer = pygame.Surface((display.get_width()-8, 2))
	timeLayer.convert()
	timer.addComponent(maze.Timer(timeLayer, time))
	timer.addComponent(component.Drawable(timer.getComponent("MazeTimer").timeLayer, 2))
	timer.addComponent(component.Script())
	timer.getComponent("Script").attach(timer.getComponent("MazeTimer").update)
	world.addEntity(timer)

	# Creating the object for the maze.
	mazeContent = world.createEntity()
	mazeContent.addComponent(component.Position((4,4)))
	mazeLayer = pygame.Surface((display.get_width()-8,display.get_height()-8))
	mazeLayer.convert()
	mazeContent.addComponent(maze.Maze(mazeLayer, cellSize))
	mazeContent.addComponent(component.Drawable(mazeContent.getComponent("Maze").mLayer, -1))
	scriptComponent = mazeContent.addComponent(component.Script())
	scriptComponent.attach(mazeContent.getComponent("Maze").update)
	world.addEntity(mazeContent)

	# Setting the walls
	mapEntity = world.createEntity()
	mapEntity.addComponent(component.Position())
	mapData = tileMap.TileMap('maze.tmx')
	tileSurface = mapData.getLayerSurface(0)
	mapEntity.addComponent(component.Drawable(tileSurface, -1))
	world.addEntity(mapEntity)

	# Creating the player
	player = world.createEntity()
	playerMarker = pygame.Surface((cellSize-1,cellSize-1)).convert()
	playerMarker.fill((255,0,0))
	player.addComponent(component.Drawable(playerMarker, 0))
	player.addComponent(component.Position((5,5)))
	player.addComponent(component.LastPosition((5,5)))

	collidable = player.addComponent(component.Collidable())
	def handleCollision(entity, event):
		currentPosition = entity.getComponent("Position")
		lastPosition = entity.getComponent("LastPosition")
		currentPosition.value = lastPosition.value
	collidable.attachHandler(handleCollision)

	playerEventHandler = player.addComponent(component.EventHandler())
	def move(entity, event):
		currentPosition = entity.getComponent("Position")
		lastPosition = entity.getComponent("LastPosition")
		if event.type == pygame.KEYDOWN:
			if keys[event.key] == "Up":
				lastPosition.value = Vector2(currentPosition.value)
				currentPosition.value += Vector2(0, -cellSize)
			elif keys[event.key] == "Down":
				lastPosition.value = Vector2(currentPosition.value)
				currentPosition.value += Vector2(0, cellSize)
			elif keys[event.key] == "Left":
				lastPosition.value = Vector2(currentPosition.value)
				currentPosition.value += Vector2(-cellSize, 0)
			elif keys[event.key] == "Right":
				lastPosition.value = Vector2(currentPosition.value)
				currentPosition.value += Vector2(cellSize, 0)
	playerEventHandler.attachHandler(pygame.KEYDOWN, move)
	world.addEntity(player)

	world.addSystem(RenderSystem(display))
	world.addSystem(ScriptSystem())
	world.addSystem(inputSystem)
	world.addSystem(TileCollisionSystem(mapData))
	return world

# Creates a world
def setupWorld(display):
	world = World()
	entity = world.createEntity()
	entity.addComponent(component.Position())
	city = pygame.image.load(os.path.join('assets', 'images', 'cityscape.png')).convert()
	entity.addComponent(component.Drawable(city, -2))
	# world.addEntity(entity)

	mapEntity = world.createEntity()
	mapEntity.addComponent(component.Position())
	mapData = tileMap.TileMap('test.tmx')
	tileSurface = mapData.getLayerSurface(0)
	mapEntity.addComponent(component.Drawable(tileSurface, -1))
	world.addEntity(mapEntity)

	playerEntity = world.createEntity()
	ghostSprite = pygame.image.load(os.path.join('assets', 'images', 'ghost.png')).convert_alpha()

	playerEntity.addComponent(component.Drawable(ghostSprite))
	playerEntity.addComponent(component.Position((8, 48)))
	playerEntity.addComponent(component.Dimension((4, 12)))
	playerEntity.addComponent(component.Velocity((0, 0)))
	playerEntity.addComponent(component.Acceleration())
	collidable = playerEntity.addComponent(component.Collidable())

	def handleCollision(entity, event):
		pass

	collidable.attachHandler(handleCollision)
	playerEntity.addComponent(component.TargetVelocity())

	# Demonstration of how to handle input.
	# We should push entity creation into its own file/function
	def handleInput(entity, event):
		global gamescreen
		targetVelocityComponent = entity.getComponent('TargetVelocity')
		velocityComponent = entity.getComponent('Velocity')
		if event.type == pygame.KEYDOWN:
			if keys[event.key] == "Left":
				targetVelocityComponent.value += Vector2(-0.5, 0)
			elif keys[event.key] == "Right":
				targetVelocityComponent.value += Vector2(0.5, 0)
			elif keys[event.key] == "Interact":
				collisionSystem = world.getSystem('TileCollisionSystem')
				collisions = collisionSystem.getEntityCollisions(entity.id)
				for other in collisions:
					if other.hasComponent('Group'):
						group = other.getComponent('Group')
						if group.value == "terminal":
							terminalDifficulty = DIFFICULTY[0] #Ideally the terminal itself should store the difficulty number.
							worlds["maze"] = setupMaze(display, terminalDifficulty)
							gamescreen = "maze"
						elif group.value == 'lift':
							originalLiftId = other.id
							liftPosition = other.getComponent('Position').value
							liftTilePosition = collisionSystem.getTilePosition(liftPosition)
							for height in range(collisionSystem.tileMap.mapSize[1]):
								entities = collisionSystem.getEntitiesInTile(liftTilePosition.x, height)
								for other in entities:
									if other.hasComponent('Group') and other.getComponent('Group').value == 'lift' \
											and other.id != originalLiftId:
										newPosition = entity.getComponent('Position').value
										liftPosition = other.getComponent('Position').value
										newPosition.y = liftPosition.y
										return
		elif event.type == pygame.KEYUP:
			if keys[event.key] == "Left":
				targetVelocityComponent.value += Vector2(+0.5, 0)
			elif keys[event.key] == "Right":
				targetVelocityComponent.value += Vector2(-0.5, 0)

		velocityComponent.value = targetVelocityComponent.value

	playerInputHandler = playerEntity.addComponent(component.EventHandler())
	playerInputHandler.attachHandler(pygame.KEYDOWN, handleInput)
	playerInputHandler.attachHandler(pygame.KEYUP, handleInput)
	world.addEntity(playerEntity)

	terminal = world.createEntity()
	termSprite = pygame.image.load(os.path.join('assets', 'images', 'terminal.png')).convert_alpha()
	terminal.addComponent(component.Position((56, 12)))
	terminal.addComponent(component.Dimension((4, 8)))
	terminal.addComponent(component.Drawable(termSprite, -1))
	terminal.addComponent(component.Collidable())
	terminal.addComponent(component.Group('terminal'))
	world.addEntity(terminal)

	liftSprite = pygame.image.load(os.path.join('assets', 'images', 'lift.png')).convert_alpha()
	doorEntity = world.createEntity()
	doorEntity.addComponent(component.Position((52, 48)))
	doorEntity.addComponent(component.Dimension((4, 12)))
	doorEntity.addComponent(component.Drawable(liftSprite, -1))
	doorEntity.addComponent(component.Collidable())
	doorEntity.addComponent(component.Group('lift'))
	world.addEntity(doorEntity)


	doorEntity = world.createEntity()
	doorEntity.addComponent(component.Position((52, 28)))
	doorEntity.addComponent(component.Dimension((4, 12)))
	doorEntity.addComponent(component.Drawable(liftSprite, -1))
	doorEntity.addComponent(component.Collidable())
	doorEntity.addComponent(component.Group('lift'))
	world.addEntity(doorEntity)

	doorEntity = world.createEntity()
	doorEntity.addComponent(component.Position((8, 8)))
	doorEntity.addComponent(component.Dimension((4, 12)))
	doorEntity.addComponent(component.Drawable(liftSprite, -1))
	doorEntity.addComponent(component.Collidable())
	doorEntity.addComponent(component.Group('lift'))
	world.addEntity(doorEntity)


	doorEntity = world.createEntity()
	doorEntity.addComponent(component.Position((8, 28)))
	doorEntity.addComponent(component.Dimension((4, 12)))
	doorEntity.addComponent(component.Drawable(liftSprite, -1))
	doorEntity.addComponent(component.Collidable())
	doorEntity.addComponent(component.Group('lift'))
	world.addEntity(doorEntity)


	world.addSystem(inputSystem)
	world.addSystem(PhysicsSystem())
	world.addSystem(TileCollisionSystem(mapData))
	world.addSystem(RenderSystem(display))
	return world

def optionsMenu(display):
	world = World()
	### NOTE: DON'T ADD ENTITES YET! ###
	# See setupMenu for the comments on this :)
	background = world.createEntity()
	background.addComponent(component.Position())
	menuImage = pygame.image.load(os.path.join('assets', 'images', 'cityscape.png')).convert()
	background.addComponent(component.Drawable(menuImage, -2))
	world.addEntity(background)

	text = world.createEntity()
	text.addComponent(component.Position())
	menuText = pygame.image.load(os.path.join('assets', 'images', 'options.png')).convert_alpha()
	text.addComponent(component.Drawable(menuText, -1))
	world.addEntity(text)

	mapEntity = world.createEntity()
	mapEntity.addComponent(component.Position())
	mapData = tileMap.TileMap('menu.tmx')
	tileSurface = mapData.getLayerSurface(0)
	mapEntity.addComponent(component.Drawable(tileSurface, -3))
	world.addEntity(mapEntity)

	musicOn = world.createEntity()
	soundOn = world.createEntity()
	musicOn.addComponent(component.Position((53,22)))
	soundOn.addComponent(component.Position((53,34)))
	onImage = pygame.image.load(os.path.join("assets", "images", "on.png"))
	musicOn.addComponent(component.Drawable(onImage, 3))
	soundOn.addComponent(component.Drawable(onImage, 3))
	if MUSIC == False:
		musicOn.getComponent("Drawable").layer = -3
	if SOUND == False:
		soundOn.getComponent("Drawable").layer = -3
	world.addEntity(musicOn)
	world.addEntity(soundOn)
	### FEEL FREE TO ADD ENTITIES AGAIN ###

	cursor = world.createEntity()
	cursor.addComponent(component.Position((2,18)))
	cursor.addComponent(component.LastPosition((2,18)))
	cursorImage = pygame.image.load(os.path.join('assets', 'images', 'cursor.png')).convert_alpha()
	cursor.addComponent(component.Drawable(cursorImage))

	collidable = cursor.addComponent(component.Collidable())
	def handleCollision(entity, event):
		currentPosition = entity.getComponent("Position")
		lastPosition = entity.getComponent("LastPosition")
		currentPosition.value = lastPosition.value
	collidable.attachHandler(handleCollision)

	cursorEventHandler = cursor.addComponent(component.EventHandler())
	def move(entity, event):
		global gamescreen, MUSIC, SOUND
		currentPosition = entity.getComponent("Position")
		lastPosition = entity.getComponent("LastPosition")
		if keys[event.key] == "Up":
			lastPosition.value = Vector2(currentPosition.value)
			currentPosition.value += Vector2(0, -12)
		elif keys[event.key] == "Down":
			lastPosition.value = Vector2(currentPosition.value)
			currentPosition.value += Vector2(0, 12)
		elif keys[event.key] in ("Interact", "Enter"):
			if currentPosition.value == Vector2(2,18):
				MUSIC = not MUSIC
				worlds[gamescreen].getEntity(3).getComponent("Drawable").layer = 0 - worlds[gamescreen].getEntity(3).getComponent("Drawable").layer
				# This swaps the value between 3 and -3 - IE visible or not.
			if currentPosition.value == Vector2(2,30):
				SOUND = not SOUND
				worlds[gamescreen].getEntity(4).getComponent("Drawable").layer = 0 - worlds[gamescreen].getEntity(4).getComponent("Drawable").layer
			else:
				print "Out of bounds D:"
	cursorEventHandler.attachHandler(pygame.KEYDOWN, move)
	world.addEntity(cursor)

	world.addSystem(RenderSystem(display))
	world.addSystem(inputSystem)
	world.addSystem(TileCollisionSystem(mapData))
	return world

def setupMenu(display):
	world = World()

	# Add the music
	pygame.mixer.music.load(os.path.join('assets','music','BlueBeat.ogg'))
	pygame.mixer.music.play(loops=-1)

	# Add the background image
	background = world.createEntity()
	background.addComponent(component.Position())
	menuImage = pygame.image.load(os.path.join('assets', 'images', 'cityscape.png')).convert()
	background.addComponent(component.Drawable(menuImage, -2))
	world.addEntity(background)

	# The text that goes on top of the world is here.
	text = world.createEntity()
	text.addComponent(component.Position())
	menuText = pygame.image.load(os.path.join('assets', 'images', 'menu.png')).convert_alpha()
	text.addComponent(component.Drawable(menuText, -1))
	world.addEntity(text)

	# We use this tmx because I (Sanchit) am too lazy to make custom collision handling :p
	mapEntity = world.createEntity()
	mapEntity.addComponent(component.Position())
	mapData = tileMap.TileMap('menu.tmx')
	tileSurface = mapData.getLayerSurface(0)
	mapEntity.addComponent(component.Drawable(tileSurface, -3))
	world.addEntity(mapEntity)

	# Add the movable component
	cursor = world.createEntity()
	cursor.addComponent(component.Position((2,22)))
	cursor.addComponent(component.LastPosition((2,22)))
	cursorImage = pygame.image.load(os.path.join('assets', 'images', 'cursor.png')).convert_alpha()
	cursor.addComponent(component.Drawable(cursorImage))
	# Which can collide with things
	collidable = cursor.addComponent(component.Collidable())
	def handleCollision(entity, event):
		currentPosition = entity.getComponent("Position")
		lastPosition = entity.getComponent("LastPosition")
		currentPosition.value = lastPosition.value
	collidable.attachHandler(handleCollision)
	# And move (a bit).
	cursorEventHandler = cursor.addComponent(component.EventHandler())
	def move(entity, event):
		global gamescreen
		currentPosition = entity.getComponent("Position")
		lastPosition = entity.getComponent("LastPosition")
		if keys[event.key] == "Up":
			lastPosition.value = Vector2(currentPosition.value)
			currentPosition.value += Vector2(0, -13)
		elif keys[event.key] == "Down":
			lastPosition.value = Vector2(currentPosition.value)
			currentPosition.value += Vector2(0, 13)
		elif keys[event.key] in ("Interact", "Enter"):
			if currentPosition.value == Vector2(2,22):
				worlds["level"] = setupWorld(display)
				gamescreen = "level"
			elif currentPosition.value == Vector2(2,35):
				worlds["options"] = optionsMenu(display)
				gamescreen = "options"
			elif currentPosition.value == Vector2(2,48):
				exit()
			else:
				print "Out of bounds D:"
		elif keys[event.key] == "Exit":
			quit()
	cursorEventHandler.attachHandler(pygame.KEYDOWN, move)
	world.addEntity(cursor)

	world.addSystem(RenderSystem(display))
	world.addSystem(inputSystem)
	world.addSystem(TileCollisionSystem(mapData))
	return world

def quitcheck(eventQueue):
	retval = 0
	global gamescreen
	for event in eventQueue:
	# Check if the user has quit, and if so quit.
		if event.type == QUIT:
			retval = 1
		elif event.type == KEYDOWN:
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

	outputSize = (512, 512)
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
