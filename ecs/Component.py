class Component:
    # Represents a component that an entity can have.
    def __init__(self, entity):
        self.entity = entity
        self._name = 'Component'
