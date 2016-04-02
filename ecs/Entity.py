class Entity:
    # Represents a game entity, which can be given components.

    def __init__(self, id):
        self.id = id
        self.components = {}

    def addComponent(self, component):
        if hasAttr(component, 'name'):
            self.components[component.name] = component
        else:
            raise ValueError('Attempted to add an object which isn\'t a component')

    def removeComponent(self, component):
        if isinstance(component, basestring):
            del self.components[component]
        elif hasAttr(component, 'name'):
            del self.components[component.name]
        else:
            raise ValueError('Attempted to remove an object which isn\'t a component')

    def hasComponent(self, component):
        if isinstance(component, basestring):
            return component in self.components
        elif hasAttr(component, 'name'):
            return component.name in self.components
        else:
            raise ValueError('Attempted to lookup an object which isn\'t a component')
