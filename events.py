from dataclasses import dataclass
import time


class Event:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.name}, de {time.strftime("%H:%M", self.start)} a {time.strftime("%H:%M", self.end)}"

    def same_name(self, name):
        return self.name.lower() == name.lower()

class EventPlanner:
    def __init__(self):
        self.events = []

    def add_event(self, name, start, end):
        event = Event(name, start, end)
        i = 0
        while i < len(self.events):
            if event.start < self.events[i].start:
                break
            i += 1

        self.events.insert(i, event)

    def list_events(self):
        return self.events
    
    def event_exists(self, name):
        return any(e.same_name(name) for e in self.events)