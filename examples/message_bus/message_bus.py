class MessageBus:
    def __init__(self):
        self._listeners = {}

    def listen(self, event_class, handler):
        self._listeners = {event_class: handler}

    def dispatch(self, event) -> None:
        for event_class, handler in self._listeners.items():
            if isinstance(event, event_class):
                handler(event)
