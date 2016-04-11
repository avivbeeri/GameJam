import pygame
from ecs import System

class ScriptSystem(System):
	def __init__(self):
		super(ScriptSystem, self).__init__();
		self.requirements = ('Script',)

	def process(self, entities, dt):
		for entity in entities:
			Script = entity.getComponent("Script")
			for script in Script.scripts:
				script(entity, dt)
