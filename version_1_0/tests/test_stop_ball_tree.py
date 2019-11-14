import unittest
from StopBallTree import StopBallTree
from stop import Stop

class TestStopBallTree(unittest.TestCase):

    def setUp(self):
        """"""
        self.ids = ['a', 'b', 'c', 'd', 'e']
        self.lat = [10, 20, 30, 40, 50]
        self.lon = [15, 30, 45, 60, 75]
        self.routes = [1, 1, 2, 2, 3]
        self.stops = [Stop(self.ids[i], self.lat[i], self.lon[i]) for i in range(len(self.ids))]

    def test_stop_2_tup(self):
        tree = StopBallTree(self.stops)
        s = [Stop('g',0,0)]
        self.assertFalse(tree.stop_2_tup(s)[0].shape == (1,2),msg='Stops returning not correct shape')
        self.assertFalse((tree.stop_2_tup(s)[0] == 0).sum() != 2,msg='Stops returning correct value')

    def test_query(self):
        tree = StopBallTree(self.stops)
        s = [Stop("g",0,0)]
        dist, matches = tree.query(s)
        self.assertTrue(matches[0] == 0)

    def test_query_radius(self):
        """
        @todo make new test data
        :return:
        """
        s = [Stop("g", 0, 0)]
        tree = StopBallTree(s)
        import math
        lat = 10 * math.pi / 180
        lon = 15 * math.pi / 180
        r = math.sqrt(lat **2 + lon ** 2)
        _ = tree.query_radius(s,r + 1)
        self.assertEqual(len(_[s[0]]),1)
        self.assertEqual(_[s[0]][0],s[0])

    def test_query_point(self):
        tree = StopBallTree(self.stops)
        matches = tree.query_point(1,1)
        print(matches)


if __name__ == '__main__':
    unittest.main()
