from .Entity import Entity

class GroupManager:
    def __init__(self, world):
        self.groups = {}
        self.world = world


    def add(self, group, entity):
        if group not in self.groups:
            self.groups[group] = set()
        self.groups[group].add(entity)

    def getAll(self, groups):
        if not hasattr(groups, '__iter__'):
            groups = (groups,)

        resultGroups = {}
        for group in groups:
            resultGroups[group] = self.get(group)

        return resultGroups

    def get(self, group):
        if group in self.groups:
            return frozenset(self.groups[group])
        else:
            return frozenset()

    def check(self, entity, group):
        if group in self.groups:
            return entity in self.groups[group]
        else:
            return False
