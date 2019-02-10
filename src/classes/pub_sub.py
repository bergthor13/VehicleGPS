class Subscriber:
    def update(self, message, data):
        '''Called when the observed object is
        modified. You call an Observable object's
        notifyObservers method to notify all the
        object's observers of the change.'''
        pass

class Publisher:
    def __init__(self, events):
        self.subscribers = { event: dict()
                             for event in events }

    def get_subscribers(self, event):
        if event in self.subscribers:
            return self.subscribers[event]

    def register(self, event, sub, callback=None):
        if callback is None:
            callback = getattr(sub, "update")
        self.get_subscribers(event)[sub] = callback
    
    def unregister(self, event, sub):
        del self.get_subscribers(event)[sub]

    def dispatch(self, event, message):
        subs = self.get_subscribers(event)
        if subs is not None:
            for subscriber, callback in list(subs.items()):
                callback(event, message)