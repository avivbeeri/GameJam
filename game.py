#!/usr/bin/env python

import math, os, pygame, random
from pygame.locals import *
from pygame.math import Vector2
from ecs import *
import component
from systems import RenderSystem, PhysicsSystem, InputSystem, TileCollisionSystem
import maze
import tileMap
from pytmx.util_pygame import load_pygame

inputSystem = InputSystem()


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
	playerEntity.addComponent(component.Position((32, 48)))
	playerEntity.addComponent(component.Dimension((4, 12)))
	playerEntity.addComponent(component.Velocity((0, 0)))
	playerEntity.addComponent(component.Acceleration())
	playerEntity.addComponent(component.Collidable())
	playerEntity.addComponent(component.TargetVelocity())

	# Demonstration of how to handle input.
	# We should push entity creation into its own file/function
	def handleInput(entity, event):
		targetVelocityComponent = entity.getComponent('TargetVelocity')
		velocityComponent = entity.getComponent('Velocity')

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				velocityComponent.value = Vector2(-0.3, 0)
				targetVelocityComponent.value = Vector2(-1, 0)
			elif event.key == pygame.K_RIGHT:
				velocityComponent.value = Vector2(0.3, 0)
				targetVelocityComponent.value = Vector2(1, 0)
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				velocityComponent.value = Vector2(0, 0)



	playerEntity.addComponent(component.EventHandler())
	playerInputHandler = playerEntity.getComponent('EventHandler')
	playerInputHandler.attachHandler(pygame.KEYDOWN, handleInput)
	playerInputHandler.attachHandler(pygame.KEYUP, handleInput)
	world.addEntity(playerEntity)

	world.addSystem(inputSystem)
	world.addSystem(PhysicsSystem())
	world.addSystem(TileCollisionSystem(mapData))
	# world.addSystem(RenderSystem(display))
	return world

def setupMaze(display):
	maze = World()

	# Creating the frame that goes around the maze.
	frame = world.createEntity()
	frame.addComponent(component.Position((0,0)))
	mazeFrame = pygame.image.load(os.path.join('assets', 'puzzleframe.png'))
	mazeFrame.convert()
	frame.addComponent(component.Drawable(mazeFrame, -1))
	maze.addEntity(frame)

	# Creating the object for the timer.
	timer = world.createEntity()
	timer.addComponent(component.Position((4,display.get_height()-4)))
	timeLayer = pygame.Surface((display.get_width()-8, 2))
	timeLayer.convert()
	timer.addComponent(component.Drawable(timeLayer, 1))
	timer.addComponent(maze.Timer())
	maze.addEntity(timer)

	# Creating the object for the maze.
	mazeContent = world.createEntity()
	mazeContent.addComponent(component.Position((4,4)))
	mazeLayer = pygame.Surface((display.get_width()-8,display.get_height()-8))
	maze.addEntity(mazeContent)

	world.addSystem(RenderSystem(display))
	return 0


def quitcheck(eventQueue, quit=True):
	for event in eventQueue:
	#Check if the user has quit, and if so quit.
		inputSystem.eventQueue.append(event)
		if event.type == QUIT:
			return 1
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				if quit == True:
					return 1
				else:
					pass
					#return to the menu
	return 0


def main():
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
	world = setupWorld(screen)
	renderSystem = RenderSystem(screen)
	eventQueue = []

	dt = (0.01) * 1000;
	accumulator = 0
	currentTime = pygame.time.get_ticks()

	while quitcheck(eventQueue) != 1:
		newTime = pygame.time.get_ticks()
		frameTime = newTime - currentTime
		currentTime = newTime
		accumulator += frameTime

		# Retrieve input events for processing
		eventQueue = pygame.event.get()
		while (accumulator >= dt):
			world.update(dt / 1000.0)
			accumulator -= dt

		# We do rendering outside the regular update loop for performance reasons
		# See: http://gafferongames.com/game-physics/fix-your-timestep/
		entities = renderSystem.getProcessableEntities(world)
		renderSystem.process(entities, 0)
		display.blit(pygame.transform.scale(screen, outputSize), (0, 0))
		pygame.display.flip()

if __name__ == '__main__': main()
