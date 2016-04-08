from .Entity import Entity

class World:
    def __init__(self):
        self.idCounter = 0
        self.entities = {}
        self.systems = []


    def createEntity(self):
        entity = Entity(self.idCounter)
        self.idCounter += 1
        return entity


    def addEntity(self, entity):
        self.entities[entity.id] = entity


    def getEntityById(self, id):
        return self.entities[id]


    def getAllEntities(self):
        return self.entities.values()


    def addSystem(self, system):
        self.systems.append(system)
        system.world = self


    def getSystem(self, systemName):
        for system in self.systems:
            if system.__class__.__name__ == systemName:
                return system
        return None


    def update(self, dt):
        for system in self.systems:
            entities = system.getProcessableEntities(self)
            system.process(entities, dt)
