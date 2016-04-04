from .Entity import Entity

class World:
    def __init__(self):
        self.idCounter = 0
        self.entities = []
        self.systems = []

    def createEntity(self):
        entity = Entity(self.idCounter)
        self.idCounter += 1
        return entity

    def addEntity(self, entity):
        self.entities.append(entity)

    def addSystem(self, system):
        self.systems.append(system)

    def getEntities(self):
        return self.entities

    def update(self, dt):
        for system in self.systems:
            entities = system.getProcessableEntities(self)
            system.process(entities, dt)
