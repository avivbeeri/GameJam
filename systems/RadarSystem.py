import pygame
from ecs import System

class ScriptSystem(System):
	def __init__(self):
		super(ScriptSystem, self).__init__();
		self.requirements = ('Radar',)

	def process(self, entities, dt):
		for entity in entities:
			Radar = entity.getComponent("Radar")
