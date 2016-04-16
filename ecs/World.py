from pygame import event
from .Entity import Entity
from .GroupManager import GroupManager
from .eventQueue import PubSub

class World(PubSub, object):
    def __init__(self):
        super(World, self).__init__()
        self.idCounter = 0
        self.entities = {}
        self.systems = []
        self.managers = { 'Group': GroupManager(self) }
        print self.eventQueue


    def createEntity(self):
        entity = Entity(self.idCounter, self)
        self.idCounter += 1
        return entity


    def addEntity(self, entity):
        self.entities[entity.id] = entity


    def getEntity(self, id):
        return self.entities[id]


    def getAllEntities(self):
        return self.entities.values()


    def addSystem(self, system):
        self.systems.append(system)
        system.onAttach(self)


    def getSystem(self, systemName):
        for system in self.systems:
            if system.__class__.__name__ == systemName:
                return system
        return None

    def getManager(self, managerType):
        return self.managers[managerType]

    def update(self, dt):
        self.eventQueue += event.get()
        for system in self.systems:
            entities = system.getProcessableEntities(self)
            system.process(entities, dt)
