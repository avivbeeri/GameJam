#!/usr/bin/env python

import math, os, pygame, random
from pygame.locals import *
from pygame.math import Vector2
from ecs import *
import component
from systems import RenderSystem, PhysicsSystem, InputSystem
import maze
import pytmx

inputSystem = InputSystem()
tmxdata = pytmx.TiledMap(os.path.join('assets', 'map.tmx'))

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
	mapSize = (64, 64)
	cellSize = 4
	tileSurface = pygame.Surface(mapSize).convert_alpha()
	tileSurface.fill((0,0,0))
	tileTotal = (mapSize[0] / cellSize) * (mapSize[1] / cellSize)
	tileMap = [None] * tileTotal
	for i in xrange((mapSize[0] / cellSize) * (mapSize[1] / cellSize)):
		tileMap[i] = 'EMPTY'
	tileMap[tileTotal - (mapSize[1] / cellSize)] =  'GROUND'
	tileColor = {
		'EMPTY': (100, 100, 100, 128),
		'GROUND': (200, 200, 200)
	}

	for i in xrange(tileTotal):
		row = i / (mapSize[0] / cellSize)
		column = i % (mapSize[0] / cellSize)
		print (row, column)
		tile = tileMap[i]
		pygame.draw.rect(tileSurface, tileColor[tile],
			pygame.Rect(column * cellSize, row * cellSize, cellSize, cellSize)
		)


	mapEntity.addComponent(component.Drawable(tileSurface, -1))
	world.addEntity(mapEntity)

	playerEntity = world.createEntity()
	ghostSprite = pygame.image.load(os.path.join('assets', 'ghost.png')).convert_alpha()

	playerEntity.addComponent(component.Drawable(ghostSprite))
	playerEntity.addComponent(component.Position((32, 48)))
	playerEntity.addComponent(component.Velocity((0, 0)))
	playerEntity.addComponent(component.Acceleration())
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
	world.addSystem(RenderSystem(display))
	return world


def setupMaze(display):
	maze = World()
	frame = world.createEntity()
	frame.addComponent(component.Position())
	mazeFrame = pygame.image.load(os.path.join('assets', 'puzzleframe.png'))
	mazeFrame.convert()

	entity.addComponent(component.Drawable(mazeFrame))
	world.addSystem(RenderSystem(display))
	return 0


def quitcheck(quit=True):
	for event in pygame.event.get():
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
	currentTime = pygame.time.get_ticks()
	dt = 1 / 60.0;
	while quitcheck() != 1:
		newTime = pygame.time.get_ticks()
		frameTime = newTime - currentTime
		currentTime = newTime

		world.update(frameTime / 1000.0)

		display.blit(pygame.transform.scale(screen, outputSize), (0, 0))
		pygame.display.flip()

if __name__ == '__main__': main()
