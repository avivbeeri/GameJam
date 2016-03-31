import pygame, random
from pygame.locals import *

class Maze:
	def __init__(self, mazeLayer):
		self.mazeArray = []
		self.state = "idle"
		self.mLayer = mazeLayer
		self.mLayer.fill((255,255,255,255))

		#We're saying that each box of the maze is 4px*4px, so there are 16x16 boxes on the screen
		for y in xrange(16):
			pygame.draw.line(self.mLayer, (255,255,255,255), (0, y*4), (64, y*4))
			for x in xrange(16):
				self.mazeArray.append(0x0000)
				if y==0:
					pygame.draw.line(self.mLayer, (255,255,255,255), (x*4, 0), (x*4, 64))
		self.totalCells = 16*16
		self.cellStack = []

	def update(self):
		if self.state == "idle":
			pass
		elif self.state == "create":
			pass

	def draw(self, screen):
		screen.blit(self.mLayer, (0,0))


