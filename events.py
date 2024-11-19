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
    
    def __eq__(self, value):
        if value is not Event:
            return False
        
        return self.same_name(value.name) and self.start == value.start and self.end == value.end

    def __repr__(self):
        return f"<{self.name}, {time.strftime("%H:%M", self.start)} - {time.strftime("%H:%M", self.end)}>"

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
    
    def find_conflicts(self):
        events = self.list_events()
        conflicts = []
        i = 0
        while i < len(events) - 1:
            e = events[i]
            conflicts_with_e = [e]
            j = i + 1
            while j < len(events) and events[j].start < e.end:
                conflicts_with_e.append(events[j])
                j += 1

            if len(conflicts_with_e) > 1:
                conflicts.append(conflicts_with_e)
            i += 1

        return conflicts
    
    def event_exists(self, name):
        return any(e.same_name(name) for e in self.events)