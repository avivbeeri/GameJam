from pygame import *
import pygame
from pygame.math import Vector2
from ecs import Component

class Visible(Component):
    pass

class Constant(Component):
    def __init__(self, value=0):
        super(Constant, self).__init__()
        self.value = value

class AccelerationConstant(Constant):
    def __init__(self, value):
        super(AccelerationConstant, self).__init__(value)
        self._name = 'Acceleration'

class Vector(Component):
    def __init__(self, vector=Vector2()):
        super(Vector, self).__init__()
        self.value = Vector2(vector)

class Acceleration(Vector):
    pass

class Position(Vector):
    pass

class LastPosition(Vector):
    pass

class Velocity(Vector):
    pass

class Dimension(Vector):
    pass

class TargetVelocity(Vector):
    pass

class Drawable(Component):
    def __init__(self, surface, layer = 0):
        super(Drawable, self).__init__()
        self.set(surface, layer)

    def set(self, surface, layer = 0):
        self.image = surface
        self.layer = layer


class EventHandler(Component):
    def __init__(self):
        super(EventHandler, self).__init__()
        self.handlers = {}

    def attachHandler(self, eventName, handler):
        if not eventName in self.handlers:
            self.handlers[eventName] = []
        self.handlers[eventName].append(handler)

    def handle(self, event):
        eventName = event.type
        if eventName in self.handlers and len(self.handlers[eventName]) > 0:
            for handler in self.handlers[eventName]:
                handler(self.entity, event)


class State(Component):
    def __init__(self, **kwargs):
        super(State, self).__init__()
        self.state = kwargs if kwargs is not None else {}

    def __getitem__(self, key):
        return self.state[key]


class Collidable(EventHandler):
    def attachHandler(self, handler):
        super(Collidable, self).attachHandler(pygame.USEREVENT, handler)


class Script(Component):
    def __init__(self):
        super(Script, self).__init__()
        self.scripts = []

    def attach(self, script):
        self.scripts.append(script)

class Radar(Component):
    def __init__(self, targetGroups):
        super(Radar, self).__init__()
        self.targetGroups = targetGroups
        self.targets = {}

    def getTargetGroups(self):
        return self.targetGroups
