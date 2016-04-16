class PubSub(object):
    def __init__(self):
        super(PubSub, self).__init__()
        self.eventQueue = []
        self.handlers = {}

    def on(self, eventTypes, handler):
        if not hasattr(eventTypes, '__iter__'):
            eventTypes = (eventTypes,)

        for eventType in eventTypes:
            if eventType not in self.handlers:
                self.handlers[eventType] = set()
            self.handlers[eventType].add(handler)

    def post(self, events):
        if not hasattr(events, '__iter__'):
            events = (events,)
        self.eventQueue += events

    def processEventQueue(self):
        for event in self.eventQueue:
            eventType = event.type
            if eventType in self.handlers:
                for handler in self.handlers[eventType]:
                    handler(event)
        del self.eventQueue[:]
