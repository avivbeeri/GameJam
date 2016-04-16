from pygame import *
import pygame
from newvector import Vector2
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
        self.flipped = False

    def set(self, surface, layer=None):
        self.image = surface
        if layer is not None:
            self.layer = layer

    def flip(self, flip=None):
        if flip is None:
            self.flipped = not self.flipped
        else:
            self.flipped = flip

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
    def __setitem__(self, key, value):
        self.state[key] = value


class SpriteState(State):
    def __init__(self, **kwargs):
        super(SpriteState, self).__init__(**kwargs)
        self.current = None


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
