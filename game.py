#!/usr/bin/env python

import os, pygame, random
from pygame.locals import *
from ecs import *
from components import AccelerationComponent,\
	VelocityComponent,\
	PositionComponent,\
	DrawableComponent
from systems import RenderSystem, PhysicsSystem
import maze

# Creates a world
def setupWorld(display):
	world = World()
	entity = world.createEntity()
	entity.addComponent(PositionComponent())
	city = pygame.image.load(os.path.join('assets', 'cityscape.png')).convert()
	entity.addComponent(DrawableComponent(city, -1))

	playerEntity = world.createEntity()
	ghostSprite = pygame.image.load(os.path.join('assets', 'ghost.png')).convert_alpha()

	playerEntity.addComponent(DrawableComponent(ghostSprite))
	playerEntity.addComponent(PositionComponent((32, 32)))
	playerEntity.addComponent(VelocityComponent((1, 0)))
	playerEntity.addComponent(AccelerationComponent())

	world.addSystem(PhysicsSystem())
	world.addSystem(RenderSystem(display))
	return world

def setupMaze(display):
	maze = World()
	frame = world.createEntity()
	frame.addComponent(PositionComponent())
	mazeFrame = pygame.image.load(os.path.join('assets', 'puzzleframe.png'))
	mazeFrame.convert()

	entity.addComponent(DrawableComponent(mazeFrame))
	world.addSystem(RenderSystem(display))
	return 0


def quitcheck(quit=True):
	for event in pygame.event.get():
	#Check if the user has quit, and if so quit.
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

	while quitcheck() != 1:
	#Mainloop that runs at 60fps.
		clock.tick(60)
		world.update()
		display.blit(pygame.transform.scale(screen, outputSize), (0, 0))
		pygame.display.flip()

if __name__ == '__main__': main()
