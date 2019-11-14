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


class TestMegaFac(unittest.TestCase):

    def test_get_megas_stops(self):
        odx = ODX(0, 1)
        odx.load_gtsf()
        day = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
        megas = odx.preprocess_gtsf(day)
        plotter = PlotStops()
        for stop in megas['51']:
            plotter.add_mega(stop)  # for s in stop.stops:  #    plotter.add_stop(s)
        for stop in megas['RAIL']:
            plotter.add_mega(stop)
        plotter.export('test.html')

    def test_process_query_results(self):
        mega_fac = MegaStopFac(100)
        result = ([[1],[1],[1]],[[1],[2],[3]])
        dist, ind = mega_fac.process_query_results(result)
        self.assertEqual(dist, [mega_fac.R,mega_fac.R, mega_fac.R])
        self.assertEqual(ind,[1,2,3])

    def test_build_ball_tree(self):
        odx = ODX(0, 1)
        odx.load_gtsf()
        day = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
        odx.preprocess_gtsf(day)
        fac = MegaStopFac(700)


    def test_correct_inbound_matches(self):
        fac = MegaStopFac(10)
        in_dist = [20,20,4,4]
        matches = [1,0,3,2]
        out = fac.correct_inbound_matches(in_dist,matches)
        self.assertEqual([0,1,7,6],out)

    def test_correct_outbound_matches(self):
        fac = MegaStopFac(10)
        in_dist = [20, 20, 4, 4]
        matches = [1, 0, 3, 2]
        out = fac.correct_outboud_matches(in_dist, matches, 4)
        self.assertEqual([4,5, 3,2], out)

    def test_get_groups(self):
        partners = [0, 1, 3, 2]
        _ = MegaStopFac(0)
        groups = _.union_find(partners)
        self.assertDictEqual(_.get_groups(groups),{0:[0],1:[1],2:[2,3]})

    def test_stop_2_tup(self):
        stops = [Stop(1,0,90)]
        _ = MegaStopFac(0)
        tup = _.stop_2_tup(stops)[0]
        self.assertAlmostEqual(tup[0],0)
        self.assertAlmostEqual(tup[1],1.5707,places=3)

    def test_build_mega_stops(self):
        stops = [Stop(1, 0, 90),Stop(2,10,45)]
        groups = {0:[0,1]}
        _ = MegaStopFac(0)
        mega_stops = _.build_mega_stops(groups,stops)
        self.assertEqual(mega_stops[0].id,"M0")
        self.assertEqual(mega_stops[0].lat,0)
        self.assertEqual(mega_stops[0].lon,90)

    def test_union_find(self):
        partners = [0,1,3,2]
        _ = MegaStopFac(0)
        self.assertListEqual(_.union_find(partners),[0,1,2,2])
        partners = [0,1,2,3]
        self.assertListEqual(_.union_find(partners), partners)


    def check_inputs(self):
        pass



if __name__ == '__main__':
    unittest.main()
