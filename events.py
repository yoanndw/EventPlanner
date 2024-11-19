from dataclasses import dataclass
import time


class Event:
    def __init__(self, name, start, end):
        self.name = name
        self.start_str = start
        self.end_str = end
        self.start = time.strptime(start, "%H:%M")
        self.end = time.strptime(end, "%H:%M")

    def __str__(self):
        return f"{self.name}, de {self.start_str} a {self.end_str}"

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