import datetime
import unittest

from events import Event, EventPlanner

class EventTest(unittest.TestCase):
    def test_constructor_strips_name(self):
        e = Event("   e  ", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))
        self.assertEqual(e.name, "e")

    def test_same_names(self):
        e1 = Event("event", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))
        self.assertTrue(e1.same_name("event"))

        e1 = Event("   \nevt", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))
        self.assertTrue(e1.same_name("evt   "))

        e1 = Event("test", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))
        self.assertTrue(e1.same_name("TEST"))

    def test_different_names(self):
        e1 = Event("evt   ", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))
        self.assertFalse(e1.same_name("    test"))

    def test_events_equal(self):
        e1 = Event("evt  ", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))
        e2 = Event("evt", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))
        self.assertEqual(e1, e2)

    def test_events_different(self):
        e1 = Event("e", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))
        e2 = Event("evt", datetime.time(hour=15, minute=00), datetime.time(hour=16, minute=00))
        self.assertNotEqual(e1, e2)

        e1 = Event("evt   ", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))
        e2 = Event("evt", datetime.time(hour=15, minute=00), datetime.time(hour=16, minute=00))
        self.assertNotEqual(e1, e2)

        e1 = Event("evt   ", datetime.time(hour=15, minute=0), datetime.time(hour=18, minute=10))
        e2 = Event("evt", datetime.time(hour=15, minute=00), datetime.time(hour=16, minute=00))
        self.assertNotEqual(e1, e2)

    def test_event_to_string(self):
        e = Event("e", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))
        self.assertEqual(str(e), "e, de 15:10 a 16:00")

        e = Event("   TeSt    ", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))
        self.assertEqual(str(e), "TeSt, de 15:10 a 16:00")

class EventPlannerTest(unittest.TestCase):
    def setUp(self):
        self.ep = EventPlanner()
    
    def test_add_unique_event(self):
        self.ep.add_event("e1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=10))
        self.assertEqual(
            self.ep.list_events(), 
            [
                Event("e1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=10)), 
            ]
        )

    def test_add_event_at_the_end(self):
        self.ep.add_event("e1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=10))
        self.ep.add_event("e2", datetime.time(hour=16, minute=30), datetime.time(hour=17, minute=00))
        self.assertEqual(
            self.ep.list_events(), 
            [
                Event("e1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=10)), 
                Event("e2", datetime.time(hour=16, minute=30), datetime.time(hour=17, minute=00))
            ]
        )

    def test_add_first_event_at_the_end(self):
        self.ep.add_event("added first", datetime.time(hour=16, minute=30), datetime.time(hour=17, minute=00))
        self.ep.add_event("added after", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=10))
        self.assertEqual(
            self.ep.list_events(), 
            [
                Event("added after", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=10)), 
                Event("added first", datetime.time(hour=16, minute=30), datetime.time(hour=17, minute=00))
            ]
        )
    
    def test_add_second_event_at_the_end(self):
        self.ep.add_event("1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=10))
        self.ep.add_event("2", datetime.time(hour=16, minute=30), datetime.time(hour=17, minute=00))
        self.ep.add_event("3", datetime.time(hour=16, minute=0), datetime.time(hour=16, minute=10))
        self.assertEqual(
            self.ep.list_events(), 
            [
                Event("1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=10)),
                Event("3", datetime.time(hour=16, minute=0), datetime.time(hour=16, minute=10)),
                Event("2", datetime.time(hour=16, minute=30), datetime.time(hour=17, minute=00)),
            ]
        )

if __name__ == "__main__":
    unittest.main()