import unittest
from odx import ODX
import datetime as dt
from schedule import ScheduleMaker
from Test.plot_stops import PlotStops
from union_find import UnionFind
from stop import Stop, MegaStop
from mega_stop_fac import MegaStopFac
from StopBallTree import StopBallTree
from network import NetworkBuilder

class TestODX(unittest.TestCase):

    def setUp(self):
        self.odx = ODX(0,1)
        self.odx.load_gtfs()
        self.day = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")

    def test_odx_preprocess_gtfs(self):
        self.assertEqual(type(self.odx.preprocess_gtfs(self.day)),dict,"gtfs MegaStops incorrect type")
        i , j = list(self.odx.megas.items())[1]
        self.assertEqual(type(i),str,"Route is incorrect Type")
        self.assertEqual(type(j), list, 'Mega Stop collection mapped to incorrect type')
        self.assertEqual(type(j[0]),MegaStop, "Megas does not have mega stops in it")
        i, j = list(self.odx.megas.items())[0]
        self.assertEqual(type(j), list, 'Mega Stop collection mapped to incorrect type')
        self.assertEqual(type(j[0]), MegaStop, "Megas does not have mega stops in it")

    def test_odx_build_network(self):
        pass


if __name__ == '__main__':
    unittest.main()