from django.utils import unittest
import django.test
from nose.tools import eq_, ok_
from mock import patch, Mock
from django.contrib.gis import geos
import datetime

from make_mozilla.events import models

class VenueTest(unittest.TestCase):
    def test_location_is_always_initialized_as_a_point_object(self):
        venue = models.Venue()
        self.assertIsNotNone(venue.location.wkt)

    def test_latitude_can_be_set(self):
        venue = models.Venue()
        venue.latitude = 51.456

        eq_(venue.location, geos.Point(0, 51.456))
    
    def test_latitude_can_be_gotten(self):
        venue = models.Venue(location = geos.Point(42, 24))

        eq_(venue.latitude, 24.0)

    def test_longitude_can_be_gotten(self):
        venue = models.Venue(location = geos.Point(42, 24))

        eq_(venue.longitude, 42.0)

    def test_longitude_can_be_set(self):
        venue = models.Venue()
        venue.longitude = 51.456

        eq_(venue.location, geos.Point(51.456, 0))

    def test_lat_lng_can_be_set_on_instantiation(self):
        venue = models.Venue(latitude = "51.0", longitude = "4")

        eq_(venue.location, geos.Point(4.0, 51.0))

class EventTest(django.test.TestCase):
    def add_event(self, name, venue, offset, public = True, verified = True):
        start = datetime.datetime.now() + datetime.timedelta(days = offset)
        end = start + datetime.timedelta(hours = 3)
        e = models.Event(name = name, venue = venue, organiser_email = 'moz@example.com',
                start = start, end = end, public = public, verified = verified)
        e.save()
        return e

    def setup_events(self):
        london = models.Venue(name = "Test Venue", street_address = "0 Somewhere St", 
                country = "GB")
        london.latitude = 51.510345
        london.longitude = -0.127072
        london.save()
        berlin = models.Venue(name = "Berlin test Venue", street_address = "Somewhere Str. 0", 
                country = "DE")
        berlin.latitude = 52.50693980
        berlin.longitude = 13.42415920
        berlin.save()

        e1 = self.add_event("E1", london, 3)
        e2 = self.add_event("E2", berlin, 2)
        e3 = self.add_event("E3", london, 1)

        eu = self.add_event("EU", berlin, 9, verified = False)
        ep = self.add_event("EP", berlin, 10, public = False)

        return (e1, e2, e3, ep)

    def test_upcoming_public_events_can_be_retrieved(self):
        (e1, e2, e3, ep) = self.setup_events()
        actual = models.Event.upcoming()
        eq_(len(actual), 3)
        ok_(e1.id in [x.id for x in actual])
        ok_(e2.id in [x.id for x in actual])

    def test_upcoming_events_near_london_can_be_retrieved(self):
        (e1, e2, e3, ep) = self.setup_events()
        actual = models.Event.near(51.5154460, -0.13165810, sort = 'start')
        eq_([x.name for x in actual], ["E3", "E1"])

    def test_upcoming_events_can_be_ordered_by_name(self):
        self.setup_events()
        actual = models.Event.upcoming(sort = 'name')
        eq_([x.name for x in actual], ["E1", "E2", "E3"])

    def test_all_upcoming_events_near_berlin_can_be_retrieved(self):
        self.setup_events()
        actual = models.Event.near(52.50693980, 13.42415920, sort = 'start', include_private = True)
        eq_([x.name for x in actual], ["E2", "EP"])
