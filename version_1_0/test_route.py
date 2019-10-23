import unittest

from stop import *
from route import Route

class RouteTestCase(unittest.TestCase):

    def setUp(self):
        ids = ['a', 'b', 'c', 'd', 'e']
        lat = [10, 20, 15, 40, 50]
        lon = [15, 30, 22.5, 60, 75]
        self.routes = [1, 1, 2, 2, 3]
        self.stops = [Stop(ids[i], lat[i], lon[i], self.routes[i]) for i in range(len(ids))]
        self.m1 = MegaStop([self.stops[0], self.stops[1]], ids[0], self.routes[0])
        self.m2 = MegaStop([self.stops[2], self.stops[3]], ids[1], self.routes[0])
        self.route = Route(1, [self.m1, self.m2])

    def test_routes_build(self):
        self.assertEqual(self.route.stops[self.m1.id], self.m1,msg="Built Stop Dictionary Error")

    def test_get_stop(self):
        self.assertEqual(self.m1,self.route.get_stop(self.m1.id))

if __name__ == '__main__':
    unittest.main()
