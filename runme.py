#!/usr/bin/env python

import pygame, random
from pygame.locals import *
import maze

def quitcheck(quit=True):
	for event in pygame.event.get():
	#Check if the user has quit, and if so quit.
		if event.type == QUIT:
			return
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				if quit == True:
					return
				else:
					pass
					#return to the menu

def main():
	pygame.init()
	screen = pygame.Surface((64, 64))
	outputSize = (128, 128)
	display = pygame.display.set_mode(outputSize)
	pygame.display.set_caption('Test')
	pygame.mouse.set_visible(0)
	#Create the window and caption etc.

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0,0,0))
	mazeFrame = pygame.image.load("assets/puzzleframe.png")
	mazeFrame.convert_alpha()
	#Make a black background for the game, and load the frame.

	mazeLayer = pygame.Surface(screen.get_size())
	mazeLayer = mazeLayer.convert_alpha() # give it some alpha values
	mazeLayer.fill((0,0,0,0))
	timeLayer = pygame.Surface((screen.get_width()-8, 2))
	timeLayer = timeLayer.convert_alpha()
	timeLayer.fill((0,0,0,0))

	screen.blit(background, (0,0))
	pygame.display.flip()
	clock = pygame.time.Clock()
	#Blit copies one layer onto another. The clock is so that we can update things.

	newmaze = maze.Maze(mazeLayer)
	newtimer = maze.Timer(timeLayer, 10)

	while True:
	#Mainloop that runs at 60fps.
		clock.tick(60)
		quitcheck()
		screen.blit(background, (0,0))
		maze.mazeupdate(screen, newmaze, mazeFrame, newtimer)
		display.blit(pygame.transform.scale(screen, outputSize), (0, 0))
		pygame.display.flip()

if __name__ == '__main__': main()
