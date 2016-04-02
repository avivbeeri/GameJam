class Entity:
    # Represents a game entity, which can be given components.

    def __init__(self, id):
        self.id = id
        self.components = {}

    def addComponent(self, component):
        if hasAttr(component, 'name'):
            self.components[component.name] = component
        else:
            # throw an error

    def removeComponent(self, component):
        if isinstance(component, basestring):
            del self.components[component]
        elif hasAttr(component, 'name'):
            del self.components[component.name]
        else:
            # Throw an error here because we have no component to remove

    def hasComponent(self, component):
        if isinstance(component, basestring):
            return component in self.components
        elif hasAttr(component, 'name'):
            return component.name in self.components
        else:
            # Throw an error here because we have no component to remove
