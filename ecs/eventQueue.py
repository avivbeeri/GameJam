class PubSub(object):
    def __init__(self):
        self.eventQueue = []
        self.handlers = {}

    def on(self, eventType, handler):
        if eventType not in self.handlers:
            self.handlers[eventType] = set()
        self.handlers[eventType].add(handler)

    def post(self, event):
        eventType = event.type
        if eventType in self.handlers:
            for handler in self.handlers[eventType]:
                handler(event)
