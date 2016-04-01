#!/usr/bin/env python

import pygame, random
from pygame.locals import *
import maze

def main():
	pygame.init()
	screen = pygame.display.set_mode((64,64))
	pygame.display.set_caption('Test')
	pygame.mouse.set_visible(0)
	#Create the window and caption etc.

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((255,255,255))
	#Make a black background for the game.

	mazeLayer = pygame.Surface(screen.get_size())
	mazeLayer = mazeLayer.convert_alpha() # give it some alpha values
	mazeLayer.fill((255,255,255,255,))

	screen.blit(background, (0,0))
	pygame.display.flip()
	clock = pygame.time.Clock()
	#I don't know what the blit thing does. The clock is so that we can update things.

	newmaze = maze.Maze(mazeLayer)

	while True:
	#Mainloop that runs at 60fps.
		clock.tick(60)
		for event in pygame.event.get():
		#Check if the user has quit, and if so quit.
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return

		newmaze.update()
		screen.blit(background, (0,0))
		newmaze.draw(screen)
		pygame.display.flip()

if __name__ == '__main__': main()