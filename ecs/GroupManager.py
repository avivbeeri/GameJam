from .Entity import Entity

class GroupManager:
    def __init__(self, world):
        self.groups = {}
        self.world = world


    def add(self, group, entity):
        if group not in self.groups:
            self.groups[group] = set()
        self.groups[group].add(entity)

    def get(self, group):
        if group in self.groups:
            return self.groups[group]
        else:
            return set()

    def check(self, entity, group):
        if group in self.groups:
            return entity in self.groups[group]
        else:
            return False
