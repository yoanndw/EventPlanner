from dataclasses import dataclass
import time


class Event:
    def __init__(self, name, start, end, conflicting=False):
        if start >= end:
            raise EventCreationException("L'evenement doit commencer au moins une minute apres son debut.")
        self.name = name.strip()
        self.start = start
        self.end = end
        self.conflicting = conflicting

    def __str__(self):
        conflict_str = "[CONFLIT] " if self.conflicting else ""
        return f"{conflict_str}{self.name}, de {self.start.strftime("%H:%M")} a {self.end.strftime("%H:%M")}"

    def same_name(self, name):
        return self.name.lower() == name.lower().strip()

    def set_conflict(self):
        self.conflicting = True
    
    def __eq__(self, value):
        if not isinstance(value, Event):
            return False
        
        return self.same_name(value.name) and self.start == value.start and self.end == value.end and self.conflicting == value.conflicting

    def __repr__(self):
        return f"<{self.name}, {self.start.strftime("%H:%M")} - {self.end.strftime("%H:%M")}, {self.conflicting}>"


class EventPlanner:
    def __init__(self):
        self.events = []

    def add_event(self, name, start, end):
        event = Event(name, start, end)
        if self._event_exists(name.strip()):
            raise EventCreationException(f"Un evenement avec le nom \"{name.strip()}\" existe deja.")

        conflicts_with_event = []
        i = 0
        while i < len(self.events) and event.start >= self.events[i].start:
            if self.events[i].end > event.start:
                self.events[i].set_conflict()
                conflicts_with_event.append(self.events[i])
            i += 1

        conflicts_with_event.extend(self._find_conflicts_forward(i, event))
        self.events.insert(i, event)

        if len(conflicts_with_event) > 0:
            event.set_conflict()

        return conflicts_with_event

    def list_events(self):
        return self.events
    
    def find_conflicts(self):
        events = self.list_events()
        conflicts = []
        i = 0
        while i < len(events) - 1:
            e = events[i]
            conflicts_with_e = self._find_conflicts_forward(i + 1, e)

            if len(conflicts_with_e) > 0:
                e.set_conflict()
                conflicts_with_e.insert(0, e)
                conflicts.append(conflicts_with_e)
            i += 1

        return conflicts
    
    def _find_conflicts_forward(self, start_index, event):
        events = self.list_events()
        conflicts_with_e = []
        j = start_index
        while j < len(events) and events[j].start < event.end:
            conflicts_with_e.append(events[j])
            events[j].set_conflict()
            j += 1
        
        return conflicts_with_e

    def _event_exists(self, name):
        return any(e.same_name(name) for e in self.events)

class EventCreationException(Exception):
    def __init__(self, message):
        super().__init__(message)
