import datetime
import unittest

from events import Event, EventCreationException, EventPlanner

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

        e = Event("E", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00), True)
        self.assertEqual(str(e), "[CONFLIT] E, de 15:10 a 16:00")

    def test_incoherent_times(self):
        with self.assertRaises(EventCreationException) as ex:
            e = Event("e", datetime.time(hour=17, minute=10), datetime.time(hour=16, minute=00))
        
        self.assertEqual(str(ex.exception), "L'evenement doit commencer au moins une minute apres son debut.")


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
        self.ep.add_event("3", datetime.time(hour=16, minute=10), datetime.time(hour=16, minute=20))
        self.assertEqual(
            self.ep.list_events(), 
            [
                Event("1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=10)),
                Event("3", datetime.time(hour=16, minute=10), datetime.time(hour=16, minute=20)),
                Event("2", datetime.time(hour=16, minute=30), datetime.time(hour=17, minute=00)),
            ]
        )

    def test_add_event_incoherent_times(self):
        with self.assertRaises(EventCreationException) as ex:
            self.ep.add_event("e", datetime.time(hour=17, minute=10), datetime.time(hour=16, minute=00))
        
        self.assertEqual(str(ex.exception), "L'evenement doit commencer au moins une minute apres son debut.")

    def test_add_event_existing_name(self):
        self.ep.add_event("e", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))
        with self.assertRaises(EventCreationException) as ex:
            self.ep.add_event("e  ", datetime.time(hour=15, minute=10), datetime.time(hour=16, minute=00))

        self.assertEqual(str(ex.exception), "Un evenement avec le nom \"e\" existe deja.")

    def test_add_event_conflict_with_other_events(self):
        self.ep.add_event("e1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=00))
        self.ep.add_event("e2", datetime.time(hour=16, minute=30), datetime.time(hour=17, minute=00))
        conflicts = self.ep.add_event("conflict", datetime.time(hour=15, minute=30), datetime.time(hour=17, minute=00))

        self.assertEqual(
            conflicts,
            [
                Event("e1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=00), True),
                Event("e2", datetime.time(hour=16, minute=30), datetime.time(hour=17, minute=00), True),
            ]
        )

        self.assertEqual(
            self.ep.list_events(),
            [
                Event("e1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=00), True),
                Event("conflict", datetime.time(hour=15, minute=30), datetime.time(hour=17, minute=00), True),
                Event("e2", datetime.time(hour=16, minute=30), datetime.time(hour=17, minute=00), True),
            ]
        )

    def test_consecutive_events_are_not_in_conflict(self):
        self.ep.add_event("e1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=00))
        self.ep.add_event("e2", datetime.time(hour=16, minute=0), datetime.time(hour=17, minute=00))
        self.assertEqual([], self.ep.find_conflicts())

    def test_find_conflicts(self):
        self.ep.add_event("e1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=00))
        self.ep.add_event("e2", datetime.time(hour=15, minute=10), datetime.time(hour=17, minute=00))

        self.ep.add_event("e3", datetime.time(hour=17, minute=5), datetime.time(hour=17, minute=15))
        self.ep.add_event("e4", datetime.time(hour=17, minute=10), datetime.time(hour=18, minute=00))
        self.assertEqual(
            self.ep.find_conflicts(),
            [
                [
                    Event("e1", datetime.time(hour=15, minute=0), datetime.time(hour=16, minute=00), True),
                    Event("e2", datetime.time(hour=15, minute=10), datetime.time(hour=17, minute=00), True)
                ],
                [
                    Event("e3", datetime.time(hour=17, minute=5), datetime.time(hour=17, minute=15), True),
                    Event("e4", datetime.time(hour=17, minute=10), datetime.time(hour=18, minute=00), True),
                ]
            ]
        )


if __name__ == "__main__":
    unittest.main()