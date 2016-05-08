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

    def getEntitiesWithComponents(self, componentNames):
        entities = self.getAllEntities()
        entitiesToProcess = []
        # if we have specific requirements, filter those entities
        if len(componentNames) > 0:
            for entity in entities:
                applicable = True
                for componentName in componentNames:
                    applicable = applicable and entity.hasComponent(componentName)

                if applicable:
                    entitiesToProcess.append(entity)

            return tuple(entitiesToProcess)

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
        self.processEventQueue()
        for system in self.systems:
            entities = system.getProcessableEntities(self)
            system.process(entities, dt)
