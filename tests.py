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

        

if __name__ == "__main__":
    unittest.main()