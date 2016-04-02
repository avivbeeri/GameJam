class Component(object):
    # Represents a component that an entity can have.
    def __init__(self):
        self._name = self.__class__.__name__
