class System:
    # Represents a system that processes entities

    def __init__(self, requirements):
        self.requirements = requirements

    def getProcessableEntities(self, world):
        entities = world.getEntities()
        entitiesToProcess = []
        # if we have specific requirements, filter those entities
        if len(requirements) > 0:
            for entity in entities:
                applicable = True
                for requirement in self.requirements:
                    applicable = applicable || entity.hasComponent(requirement)

                if applicable:
                    entitiesToProcess.append(entity)

            return entitiesToProcess
        else:
            return entities

    def process(self, entities):
        # Logic for processing entities
        pass
