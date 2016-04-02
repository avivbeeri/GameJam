from ecs import *

world = World()
entity = world.createEntity()

class NameComponent(Component):
    def __init__(self, name):
        super(NameComponent, self).__init__()
        self.value = name

class PrintSystem(System):
    def process(self, entities):
        for entity in entities:
            name = entity.getComponent('NameComponent')
            print name.value

entity.addComponent(NameComponent('Aviv'))
world.addSystem(PrintSystem([]))
world.update()
