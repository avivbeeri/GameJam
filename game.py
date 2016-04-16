#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, os, pygame, random, json
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
	elif event.type == enums.GAMEOVER:
		worlds.popitem()
		gamescreen = worlds.keys()[-1]

# Creates a world
def setupWorld(display):
	world = World()
	groupManager = world.getManager('Group')
	world.on([QUIT, KEYDOWN, enums.GAMEOVER], quitHandler)

	city = pygame.image.load(os.path.join('assets', 'images', 'cityscape.png'))
	background = auxFunctions.create(world, position=(0,0), sprite=city, layer=-1)
	world.addEntity(background)

	mapData = auxFunctions.TileMap('indoors1.tmx')
	for index, surface in enumerate(mapData.getSurfaces()):
		mapEntity = auxFunctions.create(world, position=(0,0), sprite=surface, layer=index)
		world.addEntity(mapEntity)

	entities.createGhost(world, (8, 44))

	entities.createTerminal(world, (16, 48))
	entities.createGuard(world, (8, 22))
	entities.createGuard(world, (50, 2), 2)

	entities.createStairs(world, (52, 44))
	entities.createStairs(world, (52, 24))
	entities.createStairs(world, (28, 4))
	entities.createStairs(world, (28, 24))

	entities.createPlant(world, (38, 24))

	world.addSystem(InputSystem())
	world.addSystem(RadarSystem())
	world.addSystem(ScriptSystem())
	world.addSystem(PhysicsSystem())
	world.addSystem(TileCollisionSystem(mapData))
	world.addSystem(RenderSystem(display))
	world.addSystem(SpriteSystem())
	return world

def level03(display):
	world = World()
	groupManager = world.getManager('Group')
	world.on([QUIT, KEYDOWN, enums.GAMEOVER], quitHandler)

	mapData = auxFunctions.TileMap('outdoors3.tmx')
	for index, surface in enumerate(mapData.getSurfaces()):
		mapEntity = auxFunctions.create(world, position=(0,0), sprite=surface, layer=index)
		world.addEntity(mapEntity)

	entities.createGhost(world, (4,44))
	entities.createGuard(world, (54,42))
	entities.createBin(world, (20,47))

	entities.createStairs(world, (42,44))
	entities.createStairs(world, (42,20))

	entities.createText(world, (1,1), "A guard!")
	entities.createText(world, (1,8), "I'd better")
	entities.createText(world, (1,15), "hide!")

	world.addSystem(InputSystem())
	world.addSystem(RadarSystem())
	world.addSystem(ScriptSystem())
	world.addSystem(PhysicsSystem())
	world.addSystem(TileCollisionSystem(mapData))
	world.addSystem(RenderSystem(display))
	world.addSystem(SpriteSystem())
	return world

def level02(display):
	world = World()
	groupManager = world.getManager('Group')
	world.on([QUIT, KEYDOWN, enums.GAMEOVER], quitHandler)

	mapData = auxFunctions.TileMap('outdoors2.tmx')
	for index, surface in enumerate(mapData.getSurfaces()):
		mapEntity = auxFunctions.create(world, position=(0,0), sprite=surface, layer=index)
		world.addEntity(mapEntity)

	entities.createGhost(world, (4,20))

	entities.createStairs(world, (48,44))
	entities.createStairs(world, (48,20))

	entities.createTerminal(world, (36,48))
	# A door leading to the next level would give a reason to use this terminal.

	entities.createText(world, (1,1), "Blocked.")
	entities.createText(world, (1,8), "Heading")
	entities.createText(world, (1,15), "down!")

	world.addSystem(InputSystem())
	world.addSystem(PhysicsSystem())
	world.addSystem(TileCollisionSystem(mapData))
	world.addSystem(RenderSystem(display))
	world.addSystem(SpriteSystem())
	return world

def level01(display):
	world = World()
	groupManager = world.getManager('Group')
	world.on([QUIT, KEYDOWN, enums.GAMEOVER], quitHandler)

	mapData = auxFunctions.TileMap('outdoors1.tmx')
	for index, surface in enumerate(mapData.getSurfaces()):
		mapEntity = auxFunctions.create(world, position=(0,0), sprite=surface, layer=index)
		world.addEntity(mapEntity)

	entities.createGhost(world, (4,44))
	entities.createBin(world, (34,47))

	entities.createText(world, (15,1), "If I'm")
	entities.createText(world, (10,8), "going to")
	entities.createText(world, (2,15), "get in, I'll")
	entities.createText(world, (11,23), "need to")
	entities.createText(world, (1,31), "stay hidden")

	world.addSystem(InputSystem())
	world.addSystem(PhysicsSystem())
	world.addSystem(TileCollisionSystem(mapData))
	world.addSystem(RenderSystem(display))
	world.addSystem(SpriteSystem())
	return world

def optionsMenu(display):
	world = World()
	world.on([QUIT, KEYDOWN, enums.GAMEOVER], quitHandler)
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
	cursorEventHandler.attachHandler(pygame.KEYDOWN, move)
	world.addEntity(cursor)

	world.addSystem(RenderSystem(display))
	world.addSystem(InputSystem())
	return world

def gameOver(display):
	world = World()

	menuText = pygame.image.load(os.path.join('assets', 'images', 'options.png'))
	text = auxFunctions.create(world, position=(0,0), sprite=menuText, layer=-1)
	world.addEntity(text)

	cursorImage = pygame.image.load(os.path.join('assets', 'images', 'cursor.png'))
	cursor = auxFunctions.create(world, position=(2,18), sprite=cursorImage, layer=3)

	cursorEventHandler = cursor.addComponent(component.EventHandler())
	def move(entity, event):
		global gamescreen, options
		if event.type == pygame.KEYDOWN:
			if event.key in keys:
				if keys[event.key] in ("Interact", "Enter"):
					worlds[gamescreen] = setupWorld()
	cursorEventHandler.attachHandler(pygame.KEYDOWN, move)
	world.addEntity(cursor)

	world.addSystem(RenderSystem(display))
	world.addSystem(InputSystem())
	return world

def setupMenu(display):
	world = World()
	world.on([QUIT, KEYDOWN, enums.GAMEOVER], quitHandler)

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
					worlds["level"] = level01(display)
					gamescreen = "level"
				elif currentPosition.value == Vector2(2,35):
					worlds["options"] = optionsMenu(display)
					gamescreen = "options"
				elif currentPosition.value == Vector2(2,48):
					quit()
				else:
					pass
			elif keys[event.key] == "Exit":
				pygame.quit()
	cursorEventHandler.attachHandler(pygame.KEYDOWN, move)
	world.addEntity(cursor)

	world.addSystem(RenderSystem(display))
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
