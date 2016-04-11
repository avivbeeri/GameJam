#!/usr/bin/env python

import math, os, pygame, random
import component
import maze
import tileMap
from pygame.locals import *
from pygame.math import Vector2
from ecs import *
from systems import RenderSystem, PhysicsSystem, InputSystem, ScriptSystem, TileCollisionSystem
from pytmx.util_pygame import load_pygame

inputSystem = InputSystem()
gamescreen = "main"
worlds = dict()

# Creates a world
def setupWorld(display):
	world = World()
	entity = world.createEntity()
	entity.addComponent(component.Position())
	city = pygame.image.load(os.path.join('assets', 'cityscape.png')).convert()
	entity.addComponent(component.Drawable(city, -2))
	world.addEntity(entity)

	mapEntity = world.createEntity()
	mapEntity.addComponent(component.Position())
	mapData = tileMap.TileMap('test.tmx')
	tileSurface = mapData.getLayerSurface(0)
	mapEntity.addComponent(component.Drawable(tileSurface, -1))
	world.addEntity(mapEntity)

	playerEntity = world.createEntity()
	ghostSprite = pygame.image.load(os.path.join('assets', 'ghost.png')).convert_alpha()

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
		targetVelocityComponent = entity.getComponent('TargetVelocity')
		velocityComponent = entity.getComponent('Velocity')
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				targetVelocityComponent.value += Vector2(-0.5, 0)
			elif event.key == pygame.K_RIGHT:
				targetVelocityComponent.value += Vector2(0.5, 0)
			elif event.key == pygame.K_LSHIFT:
				collisionSystem = world.getSystem('TileCollisionSystem')
				collisions = collisionSystem.getEntityCollisions(entity.id)
				for other in collisions:
					if other.hasComponent('Group'):
						group = other.getComponent('Group')
						print group.value
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				targetVelocityComponent.value += Vector2(+0.5, 0)
			elif event.key == pygame.K_RIGHT:
				targetVelocityComponent.value += Vector2(-0.5, 0)

		velocityComponent.value = targetVelocityComponent.value

	playerInputHandler = playerEntity.addComponent(component.EventHandler())
	playerInputHandler.attachHandler(pygame.KEYDOWN, handleInput)
	playerInputHandler.attachHandler(pygame.KEYUP, handleInput)
	world.addEntity(playerEntity)

	terminal = world.createEntity()
	termSprite = pygame.image.load(os.path.join('assets', 'terminal.png')).convert_alpha()
	terminal.addComponent(component.Position((56, 52)))
	terminal.addComponent(component.Dimension((4, 8)))
	terminal.addComponent(component.Drawable(termSprite, -1))
	terminal.addComponent(component.Collidable())
	terminal.addComponent(component.Group('terminal'))
	world.addEntity(terminal)

	world.addSystem(inputSystem)
	world.addSystem(PhysicsSystem())
	world.addSystem(TileCollisionSystem(mapData))
	# world.addSystem(RenderSystem(display))
	return world

def setupMaze(display, time, cellSize):
	world = World()

	# Creating the frame that goes around the maze.
	frame = world.createEntity()
	frame.addComponent(component.Position((0,0)))
	mazeFrame = pygame.image.load(os.path.join('assets', 'puzzleframe.png'))
	mazeFrame.convert()
	frame.addComponent(component.Drawable(mazeFrame, 1))
	frame.addComponent(component.Collidable())
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
	mapEntity.addComponent(component.Drawable(tileSurface, 2))
	world.addEntity(mapEntity)

	# Creating the player
	player = world.createEntity()
	playerMarker = pygame.Surface((cellSize-1,cellSize-1)).convert()
	playerMarker.fill((255,0,0))
	player.addComponent(component.Drawable(playerMarker, 0))
	player.addComponent(component.Position((5,5)))
	player.addComponent(component.LastPosition((5,5)))
	player.addComponent(component.Velocity((0,0)))
	playerEventHandler = player.addComponent(component.EventHandler())

	collidable = player.addComponent(component.Collidable())
	def handleCollision(entity, event):
		print "Collided!"
		currentPosition = entity.getComponent("Position")
		lastPosition = entity.getComponent("LastPosition")
		currentPosition.value = lastPosition.value
	collidable.attachHandler(handleCollision)

	playerEventHandler = player.addComponent(component.EventHandler())
	def move(entity, event):
		currentPosition = entity.getComponent("Position")
		lastPosition = entity.getComponent("LastPosition")
		if event.type == pygame.KEYDOWN:
			if event.key == K_UP:
				lastPosition.value = currentPosition.value
				currentPosition.value += Vector2(0, -cellSize)
			elif event.key == K_DOWN:
				lastPosition.value = currentPosition.value
				currentPosition.value += Vector2(0, cellSize)
			elif event.key == K_LEFT:
				lastPosition.value = currentPosition.value
				currentPosition.value += Vector2(-cellSize, 0)
			elif event.key == K_RIGHT:
				lastPosition.value = currentPosition.value
				currentPosition.value += Vector2(cellSize, 0)
		print "Current Position is " + str(currentPosition.value) + " and previous position is " + str(lastPosition.value)
	playerEventHandler.attachHandler(pygame.KEYDOWN, move)
	world.addEntity(player)

	world.addSystem(RenderSystem(display))
	world.addSystem(ScriptSystem())
	world.addSystem(inputSystem)
	world.addSystem(TileCollisionSystem(mapData))
	return world


def quitcheck(eventQueue, quit=True):
	retval = 0
	for event in eventQueue:
	#Check if the user has quit, and if so quit.

		if event.type == QUIT:
			retval = 1
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				if quit == True:
					retval = 1
				else:
					pass # In future we'll use this to return to the main menu
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
	worlds["main"] = setupWorld(screen)
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
		for event in eventQueue:
			if (event.type == KEYDOWN) and (event.key == K_SPACE):
				if gamescreen == "main":
					worlds["maze"] = setupMaze(screen, 15, 4)
					gamescreen = "maze"
				elif gamescreen == "maze":
					worlds.pop("maze", None)
					gamescreen = "main"
			if (event.type == USEREVENT) and (event.code == "TIMERQUIT"):
				worlds.pop("maze", None)
				gamescreen = "main"
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
