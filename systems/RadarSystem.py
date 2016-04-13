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
			radar.targets.clear()
			targetGroups = groupManager.getAll(radar.getTargetGroups())
			entityPosition = entity.getComponent('Position').value
			# TODO: Use the Radar config to decide if we need to fire an event
			for key, group in targetGroups.iteritems():
				radar.targets[key] = set()
				for target in group:
					if not target.hasComponent('Visible'):
						continue
					ping = self.RadarPing()
					ping.group = key
					ping.entity = target
					targetPosition = target.getComponent('Position').value
					ping.position = targetPosition
					ping.distance = targetPosition - entityPosition
					radar.targets[key].add(ping)

			'''
			player = next(iter(targets['player']))
			entityPosition = entity.getComponent('Position').value
			entityDirection = entity.getComponent('State').direction
			playerPosition = player.getComponent('Position').value
			if entityPosition.y == playerPosition.y and \
					entityPosition.x < playerPosition.x and \
					entityDirection == 'right':
				print 'ALERT'
			'''

	class RadarPing(object):
		pass
