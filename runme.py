#!/usr/bin/env python

import pygame, random
from pygame.locals import *

def main():
	pygame.init()
	screen = pygame.display.set_mode((64,64))
	pygame.display.set_caption('Test')
	pygame.mouse.set_visible(0)
	#Create the window and caption etc.

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0,0,0))
	#Make a black background for the game.

	screen.blit(background, (0,0))
	pygame.display.flip()
	clock = pygame.time.Clock()
	#I don't know what the blit thing does. The clock is so that we can update things.

	while True:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return
		screen.blit(background, (0,0))
		pygame.display.flip()

if __name__ == '__main__': main()