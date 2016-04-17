#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, os, pygame, random, json, sys
import component
import auxFunctions
import entities
from collections import OrderedDict
from pygame.locals import *
from newvector import Vector2
from ecs import *
from systems import *
from pytmx.util_pygame import load_pygame
from util.enums import keys
from util import enums


with open('options.json', "r") as f:
	options = json.load(f)

gamescreen = "menu"
worlds = OrderedDict()


def quitHandler(event):
	global gamescreen
	if event.type == QUIT:
		quit()
	elif event.type == KEYDOWN:
		if event.key in keys:
			if keys[event.key] == "Exit":
				worlds.popitem()
				if len(worlds) == 0:
					quit()
				gamescreen = worlds.keys()[-1]

# Creates a world

def createWorld(levelFile):
	world = World()
	world.on([QUIT, KEYDOWN], quitHandler)

	def gameOverHandler(event):
		if event.type == enums.GAMEOVER:
			pygame.time.wait(1000)
			worlds["level"] = gameOver()
	world.on([enums.GAMEOVER], gameOverHandler)

	def offscreenHandler(event):
		if event.edge != 'RIGHT':
			return
		groupManager = world.getManager('Group')
		terminals = groupManager.get('terminal')
		success = True
		for terminal in terminals:
			success = success and terminal.getComponent('SpriteState').current == 'win'
		if success:
			event = pygame.event.Event(enums.LEVELCOMPLETE)
			world.post(event)
	world.on(enums.OFFSCREEN, offscreenHandler)

	mapData = auxFunctions.TileMap(levelFile)
	for index, surface in enumerate(mapData.getSurfaces()):
		mapEntity = auxFunctions.create(world, position=(0,0), sprite=surface, layer=index)
		world.addEntity(mapEntity)

	world.addSystem(InputSystem())
	world.addSystem(InteractionSystem())
	world.addSystem(RadarSystem())
	world.addSystem(ScriptSystem())
	world.addSystem(PhysicsSystem())
	world.addSystem(TileCollisionSystem(mapData))
	world.addSystem(SpriteSystem())
	world.addSystem(SoundSystem(world, options['SOUND']))
	return world

def setupWorld():
	world = createWorld('indoors1.tmx')

	def levelCompleteHandler(event):
		if event.type == enums.LEVELCOMPLETE:
			pygame.time.wait(1000)
			worlds["level"] = missionComplete(level01)
	world.on([enums.LEVELCOMPLETE], levelCompleteHandler)

	city = pygame.image.load(os.path.join('assets', 'images', 'cityscape.png'))
	background = auxFunctions.create(world, position=(0,0), sprite=city, layer=-1)
	world.addEntity(background)

	entities.createGhost(world, (8, 44))

	entities.createGuard(world, (8, 22))
	entities.createGuard(world, (50, 2), 2)

	entities.createStairs(world, (52, 44))
	entities.createStairs(world, (52, 24))
	entities.createStairs(world, (28, 4))
	entities.createStairs(world, (28, 24))

	entities.createPlant(world, (38, 24))

	entities.createTerminal(world, (16, 8))

	return world

def level04():
	world = createWorld('indoors2.tmx')
	def levelCompleteHandler(event):
		if event.type == enums.LEVELCOMPLETE:
			pygame.time.wait(1000)
			worlds["level"] = missionComplete(setupWorld)
	world.on([enums.LEVELCOMPLETE], levelCompleteHandler)

	entities.createGhost(world, (8,44))

	entities.createGuard(world, (28,22))

	entities.createStairs(world, (12,44))
	entities.createStairs(world, (12,24))
	entities.createStairs(world, (12,4))
	entities.createPlant(world, (2,24))
	entities.createTerminal(world, (5,8))

	entities.createStairs(world, (44,44))
	entities.createStairs(world, (44,24))
	entities.createPlant(world, (50,24))
	entities.createStairs(world, (44,4))

	entities.createTerminal(world, (36,8))

	return world

def level03():
	world = createWorld('outdoors3.tmx')

	entities.createGhost(world, (4,44))
	entities.createGuard(world, (54,42))
	entities.createBin(world, (20,47))

	entities.createStairs(world, (42,44))
	entities.createStairs(world, (42,20))

	entities.createText(world, (1,1), "A guard! I'd")
	entities.createText(world, (1,8), "better hide!")

	def levelCompleteHandler(event):
		if event.type == enums.LEVELCOMPLETE:
			pygame.time.wait(1000)
			worlds["level"] = missionComplete(level04)
	world.on([enums.LEVELCOMPLETE], levelCompleteHandler)


	return world

def level02():
	world = createWorld('outdoors2.tmx')
	groupManager = world.getManager('Group')

	entities.createGhost(world, (4,20))

	entities.createStairs(world, (48,44))
	entities.createStairs(world, (48,20))

	entities.createTerminal(world, (36,48))

	def levelCompleteHandler(event):
		if event.type == enums.LEVELCOMPLETE:
			pygame.time.wait(1000)
			worlds["level"] = missionComplete(level03)
	world.on([enums.LEVELCOMPLETE], levelCompleteHandler)

	return world

def level01():
	world = createWorld('outdoors1.tmx')

	def levelCompleteHandler(event):
		if event.type == enums.LEVELCOMPLETE:
			pygame.time.wait(1000)
			worlds["level"] = missionComplete(level02)
	world.on([enums.LEVELCOMPLETE], levelCompleteHandler)

	entities.createGhost(world, (4,44))
	entities.createBin(world, (34,47))

	entities.createText(world, (4,1), "If I'm going")
	entities.createText(world, (8,8), "to get in,")
	entities.createText(world, (3,15), "I'll need to")
	entities.createText(world, (1,23), "stay hidden.")

	return world

def optionsMenu(display):
	world = World()
	world.on([QUIT, KEYDOWN], quitHandler)
	### NOTE: DON'T ADD ENTITES YET! ###
	# See setupMenu for the comments on this :)
	menuImage = pygame.image.load(os.path.join('assets', 'images', 'cityscape.png'))
	background = auxFunctions.create(world, position=(0,0), sprite=menuImage, layer=-2)
	world.addEntity(background)

	menuText = pygame.image.load(os.path.join('assets', 'images', 'options.png'))
	text = auxFunctions.create(world, position=(0,0), sprite=menuText, layer=-1)
	world.addEntity(text)

	onImage = pygame.image.load(os.path.join("assets", "images", "on.png"))
	musicOn = auxFunctions.create(world, position=(53,22), sprite=onImage, layer=3)
	soundOn = auxFunctions.create(world, position=(53,34), sprite=onImage, layer=3)
	if options["MUSIC"] == False:
		musicOn.getComponent("Drawable").layer = -3
	if options["SOUND"] == False:
		soundOn.getComponent("Drawable").layer = -3
	world.addEntity(musicOn)
	world.addEntity(soundOn)
	### FEEL FREE TO ADD ENTITIES AGAIN ###

	cursorImage = pygame.image.load(os.path.join('assets', 'images', 'cursor.png'))
	cursor = auxFunctions.create(world, position=(2,18), sprite=cursorImage, layer=3)

	cursorEventHandler = cursor.addComponent(component.EventHandler())
	def move(entity, event):
		global gamescreen, options
		currentPosition = entity.getComponent("Position")
		if event.key in keys:
			if keys[event.key] == "Up":
				if currentPosition.value[1] > 18:
					currentPosition.value += Vector2(0, -12)
			elif keys[event.key] == "Down":
				if currentPosition.value[1] < 30:
					currentPosition.value += Vector2(0, 12)
			elif keys[event.key] in ("Interact", "Enter"):
				if currentPosition.value[1] == 18:
					options["MUSIC"] = not options["MUSIC"]
					worlds[gamescreen].getEntity(2).getComponent("Drawable").layer = 0 - \
							worlds[gamescreen].getEntity(2).getComponent("Drawable").layer
					# This swaps the value between 3 and -3 - IE visible or not.
					if options["MUSIC"] == True:
						pygame.mixer.music.play(-1)
					else:
						pygame.mixer.music.stop()
				elif currentPosition.value[1] == 30:
					options["SOUND"] = not options["SOUND"]
					worlds[gamescreen].getEntity(3).getComponent("Drawable").layer = 0 - \
							worlds[gamescreen].getEntity(3).getComponent("Drawable").layer
				else:
					pass
			with open('options.json', "w") as f:
				json.dump(options, f, indent=4)
	cursorEventHandler.attach(pygame.KEYDOWN, move)
	world.addEntity(cursor)

	# world.addSystem(RenderSystem(display))
	world.addSystem(InputSystem())
	return world

def gameOver():
	world = World()
	world.on([QUIT, KEYDOWN], quitHandler)
	entities.createText(world, (13, 0), "MISSION")
	entities.createText(world, (17, 8), "FAILED")
	entities.createText(world, (2, 24), "PRESS ENTER TO")
	entities.createText(world, (6, 32), "TRY AGAIN")

	inputEntity = world.createEntity()
	inputEventHandler = inputEntity.addComponent(component.EventHandler())
	def move(entity, event):
		global gamescreen, options
		if event.type == pygame.KEYDOWN:
			if event.key in keys:
				if keys[event.key] in ("Interact", "Enter"):
					worlds[gamescreen] = setupWorld()

	inputEventHandler.attach(pygame.KEYDOWN, move)
	world.addEntity(inputEntity)

	world.addSystem(InputSystem())
	return world

def missionComplete(nextWorldFunc):
	world = World()
	world.on([QUIT, KEYDOWN], quitHandler)
	entities.createText(world, (13, 0), "MISSION")
	entities.createText(world, (11, 8), "SUCCESS")
	entities.createText(world, (2, 24), "PRESS ENTER TO")
	entities.createText(world, (9, 32), "CONTINUE")

	inputEntity = world.createEntity()
	inputEventHandler = inputEntity.addComponent(component.EventHandler())
	def move(entity, event):
		global gamescreen, options
		if event.type == pygame.KEYDOWN:
			if event.key in keys:
				if keys[event.key] in ("Interact", "Enter"):
					worlds[gamescreen] = nextWorldFunc()

	inputEventHandler.attach(pygame.KEYDOWN, move)
	world.addEntity(inputEntity)

	world.addSystem(InputSystem())
	return world

def setupMenu(display):
	world = World()
	world.on([QUIT, KEYDOWN], quitHandler)

	# Add the music
	pygame.mixer.music.load(os.path.join('assets','music','BlueBeat.wav'))
	if options["MUSIC"] == True:
		pygame.mixer.music.play(-1)

	# Add the background image
	menuImage = pygame.image.load(os.path.join('assets', 'images', 'cityscape.png'))
	background = auxFunctions.create(world, position=(0,0), sprite=menuImage, layer=-2)
	world.addEntity(background)

	# The text that goes on top of the world is here.
	menuText = pygame.image.load(os.path.join('assets', 'images', 'menu.png'))
	text = auxFunctions.create(world, position=(0,0), sprite=menuText, layer=-1)
	world.addEntity(text)

	# Add the movable component
	cursorImage = pygame.image.load(os.path.join('assets', 'images', 'cursor.png'))
	cursor = auxFunctions.create(world, position=(2,22), lastPosition=(2,22), sprite=cursorImage, layer=0)
	# Which can move (a bit).
	cursorEventHandler = cursor.addComponent(component.EventHandler())
	def move(entity, event):
		global gamescreen
		currentPosition = entity.getComponent("Position")
		if event.key in keys:
			if keys[event.key] == "Up":
				if currentPosition.value[1] > 22:
					currentPosition.value += Vector2(0, -13)
			elif keys[event.key] == "Down":
				if currentPosition.value[1] < 48:
					currentPosition.value += Vector2(0, 13)
			elif keys[event.key] in ("Interact", "Enter"):
				if currentPosition.value == Vector2(2,22):
					worlds["level"] = level04()
					gamescreen = "level"
				elif currentPosition.value == Vector2(2,35):
					worlds["options"] = optionsMenu(display)
					gamescreen = "options"
				elif currentPosition.value == Vector2(2,48):
					sys.exit()
				else:
					pass
			elif keys[event.key] == "Exit":
				sys.exit()
	cursorEventHandler.attach(pygame.KEYDOWN, move)
	world.addEntity(cursor)

	# world.addSystem(RenderSystem(display))
	world.addSystem(InputSystem())
	return world

def main():
	global gamescreen, worlds
	pygame.init()

	outputSize = (options["SIZE"], options["SIZE"])
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
	worlds["menu"] = setupMenu(screen)

	# Set up our render system, which we share between all worlds
	renderSystem = RenderSystem(screen)

	dt = (1.0 / 60.0) * 1000;
	accumulator = 0
	currentTime = pygame.time.get_ticks()

	while True:
		newTime = pygame.time.get_ticks()
		frameTime = newTime - currentTime
		currentTime = newTime
		accumulator += frameTime

		# Retrieve input events for processing and pass them to the world
		worlds[gamescreen].post(pygame.event.get())
		renderSystem.world = worlds[gamescreen]
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
