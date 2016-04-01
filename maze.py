import pygame, random
from pygame.locals import *

class Maze:
	def __init__(self, mazeLayer):
		self.mazeArray = []
		self.state = "create"
		self.mLayer = mazeLayer
		self.mLayer.fill((0,0,0,0))

		#We're saying that each box of the maze is 4px*4px, so there are 16x16 boxes on the screen
		for y in xrange(16):
			pygame.draw.line(self.mLayer, (0,0,0,255), (0, y*4), (64, y*4))
			for x in xrange(16):
				self.mazeArray.append(0)
				if y==0:
					pygame.draw.line(self.mLayer, (0,0,0,255), (x*4, 0), (x*4, 64))
		self.totalCells = 16*16
		self.currentCell = random.randint(0, self.totalCells-1)
		self.visitedCells = 1
		self.cellStack = []
		self.compass = [(-1,0),(0,1),(1,0),(0,-1)]

	def update(self):
		if self.state == "idle":
			pass
		elif self.state == "create":
			#while VisitedCells < TotalCells
			if self.visitedCells >= self.totalCells:
				self.currentCell = 0
				self.cellStack = []
				self.state = "idle"
				return

			moved = False
			while moved == False:
				x = self.currentCell % 16
				y = self.currentCell / 16

				#Find all neighbours of current cell
				neighbors = []
				for i in xrange(4):
					nx = x + self.compass[i][0]
					ny = y + self.compass[i][1]
					#Check if all its walls are intact
					if ((nx >= 0) and (ny >= 0) and (nx < 16) and (ny < 16)):
						# Has it been visited?
						if (self.mazeArray[(ny*16+nx)] & 0x000F) == 0:
							nidx = ny*16+nx
							neighbors.append((nidx,1<<i))

				#If one or more neighbours have been found, choose one at random:
				if len(neighbors) > 0:
					idx = random.randint(0,len(neighbors)-1)
					nidx,direction = neighbors[idx]

					#knock down the wall between it and CurrentCell
					dx = x*4
					dy = y*4
					if direction & 1: # if direction is West
						self.mazeArray[nidx] |= (4) # knock down the East
						pygame.draw.line(self.mLayer, (0,0,0,0), (dx,dy+1),(dx,dy+3))
					elif direction & 2: # if the direction is South
						self.mazeArray[nidx] |= (8) # knock down the North
						pygame.draw.line(self.mLayer, (0,0,0,0), (dx+1,dy+4),(dx+3,dy+4))
					elif direction & 4: # if direction is east
						self.mazeArray[nidx] |= (1) # knock down the West
						pygame.draw.line(self.mLayer, (0,0,0,0), (dx+4,dy+1),(dx+4,dy+3))
					elif direction & 8: # if direction is North
						self.mazeArray[nidx] |= (2) # knock down the South
						pygame.draw.line(self.mLayer, (0,0,0,0), (dx+1,dy),(dx+3,dy))
					self.mazeArray[self.currentCell] |= direction

					#push CurrentCell location on the CellStack 
					self.cellStack.append(self.currentCell)
					#make the new cell CurrentCell 
					self.currentCell = nidx
					#add 1 to VisitedCells
					self.visitedCells = self.visitedCells + 1
					moved = True

				else:
				#Make the most recent cell the current cell.
					self.currentCell = self.cellStack.pop()

	def draw(self, screen):
		screen.blit(self.mLayer, (0,0))


