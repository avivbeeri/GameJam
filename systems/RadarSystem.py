import pygame
from ecs import System

class RadarSystem(System):
	def __init__(self):
		super(RadarSystem, self).__init__();
		self.requirements = ('Radar',)

	def process(self, entities, dt):
		groupManager = self.world.getManager('Group')
		for entity in entities:
			radar = entity.getComponent("Radar")
			targets = groupManager.getAll(radar.getTargets())

			# TODO: Use the Radar config to decide if we need to fire an event

			player = next(iter(targets['player']))
			entityPosition = entity.getComponent('Position').value
			entityDirection = entity.getComponent('State').direction
			playerPosition = player.getComponent('Position').value
			if entityPosition.y == playerPosition.y and \
					entityPosition.x < playerPosition.x and \
					entityDirection == 'right':
				print 'ALERT'
