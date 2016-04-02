import Entity

class World:
    def __init__(self):
        self.idCounter = 0
        self.entities = []
        self.systems = []

    def createEntity(self):
        entity = Entity(idCounter)
        idCounter += 1
        self.entities.append(entity)
        return entity

    def addSystem(self, system):
        self.systems.append(system)

    def getEntities(self):
        return self.entities

    def update(self):
        for system in self.systems:
            entities = system.getProcessableEntities()
            system.process(entities)
