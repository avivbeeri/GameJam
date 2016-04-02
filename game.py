#!/usr/bin/env python

import os, pygame, random
from pygame.locals import *
from ecs import *
from components import *
from systems import *

# Creates a world
def setupWorld(display):
	world = World()
	entity = world.createEntity()
	entity.addComponent(PositionComponent())
	city = pygame.image.load(os.path.join('assets', 'cityscape.png'))

	entity.addComponent(DrawableComponent(city))
	world.addSystem(RenderSystem(display))


	return world


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
	screen = pygame.Surface((64, 64))
	screen.fill((0,0,0))
	screen = screen.convert()

	# Initalise the game loop clock
	clock = pygame.time.Clock()

	# Create the world
	# Later this could be delegated to a "State" object.
	world = setupWorld(screen)

	while True:
	#Mainloop that runs at 60fps.
		clock.tick(60)
		if quitcheck() == 1:
			return
		world.update()
		display.blit(pygame.transform.scale(screen, outputSize), (0, 0))
		pygame.display.flip()

if __name__ == '__main__': main()
