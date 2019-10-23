"""
@author Joshua E. Morgan , jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
"""

import unittest
from odx import ODX
import datetime as dt
from schedule import ScheduleMaker
from plot_stops import PlotStops
from union_find import UnionFind
from stop import Stop, MegaStop, TrainStop, BusStop
from mega_stop_fac import MegaStopFac
from StopBallTree import StopBallTree
from network_builder import NetworkBuilder


class TestODX(unittest.TestCase):

    def setUp(self):
        self.odx = ODX(0,1)
        self.odx.load_gtsf()
        self.day = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")

    def test_odx_preprocess_gtsf(self):
        self.assertEqual(type(self.odx.preprocess_gtsf(self.day)),dict,"GTSF MegaStops incorrect type")
        i , j = list(self.odx.megas.items())[1]
        self.assertEqual(type(i),str,"Route is incorrect Type")
        self.assertEqual(type(j), list, 'Mega Stop collection mapped to incorrect type')
        self.assertEqual(type(j[0]),MegaStop, "Megas does not have mega stops in it")
        i, j = list(self.odx.megas.items())[0]
        self.assertEqual(type(j), list, 'Mega Stop collection mapped to incorrect type')
        self.assertEqual(type(j[0]), MegaStop, "Megas does not have mega stops in it")

    def test_odx_build_network(self):
        pass

class TestUnionFind(unittest.TestCase):

    def test_union(self):
        uf = UnionFind([i for i in range(0,10)])
        unions = [0,2,3,3,5,5,5,5,5,5]
        for i,j in enumerate(unions):
            uf.union(i,j)

        self.assertEqual(uf.ids, [0,1,1,1,4,4,4,4,4,4], msg='Union Find merge incorrect')
        self.assertEqual(uf.find(2), 1,msg='Union find incorrect finds the representative class')

class TestRailFac(unittest.TestCase):

    pass
    """def test_get_train_stops(self):
        from Rail_stop_fac import RailStopFac
        odx = ODX(0, 1)
        odx.load_gtsf()
        day = dt.datetime.strptime("02/08/18 00:00", "%m/%d/%y %H:%M")
        megas = odx.preprocess_gtsf(day)
        plotter = PlotStops()
        rsf = RailStopFac(200)
        for stop in rsf.get_rail_stops(odx.scheduler.get_trains_dict()):
            plotter.add_mega(stop)
        plotter.export("test1.html")
    """




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

class TestStop(unittest.TestCase):
    """
    """

    def setUp(self):
        """"""
        self.ids = ['a', 'b', 'c', 'd', 'e']
        self.lat = [10, 20, 30, 40, 50]
        self.lon = [15, 30, 45, 60, 75]
        self.routes = [1, 1, 2, 2, 3]

    def test_stop(self):
        stops = [Stop(self.ids[i], self.lat[i], self.lon[i]) for i in range(len(self.ids))]
        self.assertEqual(stops[0].to_tuple(), ('a', 10, 15), msg='Stop 2 Tuple Not working')
        self.assertEqual(stops[0] == stops[1], False,msg='Stops equivalent not working')
        self.assertEqual(hash(stops[0]),hash(self.ids[0]),msg='Stops hash not working')
        self.assertEqual(stops[0] > stops[1],False, msg="Stops greater than not working")
        self.assertEqual(stops[0] < stops[1],True, msg="Stops less than not working")

    def test_mega_stop(self):
        stops = [Stop(self.ids[i], self.lat[i], self.lon[i]) for i in range(len(self.ids))]
        m1 = MegaStop(self.ids[0], [stops[0], stops[1]],True)
        self.assertEqual(m1.lat, 15)
        self.assertEqual(m1.lon, 22.5)
        self.assertEqual(m1.to_tuple(), ('a', 15, 22.5))
        m1 = MegaStop(self.ids[0], [stops[0], stops[1]])
        self.assertEqual(m1.lat,10)
        self.assertEqual(m1.lon,15)

    def test_train_stop(self):
        pass

    def test_bus_stop(self):
        pass

class TestSchedule(unittest.TestCase):

    def test_import_files(self):
        odx = ODX(0,1)
        odx.load_gtsf()
        scheduler = ScheduleMaker(odx.gtsf['trips'], odx.gtsf['calendar'], odx.gtsf['stop_times'], odx.gtsf['stops'],
                      odx.gtsf['routes'])
        #@todo change test format to make sure key columns are in the set
        #self.assertListEqual(list(scheduler.cal.columns),['service_id','monday','tuesday','wednesday','thursday','friday','saturday','sunday','start_date','end_date'])
        #self.assertListEqual(list(scheduler.stop_times.columns),['trip_id','arrival_time','departure_time','stop_id','stop_sequence'])
        #self.assertListEqual(list(scheduler.stops.columns),['stop_id','stop_code','stop_name','stop_lat','stop_lon'])
        #self.assertListEqual(list(scheduler.routes.columns), ['route_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_desc', 'route_type','route_url','route_color','route_text_color'])
        #self.assertListEqual(list(scheduler.trips.columns),['route_id','service_id','trip_id','direction_id','block_id','shape_id'])



    def test_schedule_maker(self):
        """
        :return:
        """
        odx = ODX(0, 1)
        odx.load_gtsf()
        scheduler = ScheduleMaker(odx.gtsf['trips'], odx.gtsf['calendar'], odx.gtsf['stop_times'], odx.gtsf['stops'],
                                  odx.gtsf['routes'])
        day = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
        train, bus = scheduler.build_daily_table(day)


    def test_daily_table(self):
        #@test
        pass

    def get_service_type(self):
        #@test
        pass

    def get_routes(self):
        #@test
        pass

class TestPlotStops(unittest.TestCase):

    def test_init(self):
        pass

    def test_add_stop(self):
        pass

    def test_add_mega(self):
        pass

    def test_export(self):
        pass

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
        pass
        s = [Stop("g", 0, 0)]
        tree = StopBallTree(s)
        import math
        lat = 10 * math.pi / 180
        lon = 15 * math.pi / 180
        r = math.sqrt(lat **2 + lon ** 2)
        _ = tree.query_radius(s,r + 1)
        self.assertEqual(len(_[s[0]]),1)
        self.assertEqual(_[s[0]][0],s[0])

class TestNetworkBuild(unittest.TestCase):

    def setUp(self):
        odx = ODX(0, 1)
        odx.load_gtsf()
        day = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
        self.megas = odx.preprocess_gtsf(day)


    def test_build(self):
        builder = NetworkBuilder(700)
        net = builder.build(self.megas,1)
        #self.assertEqual(net.routes["RAIL"].stops[908480].id, 908480,msg='Object build incorrectly')

    def test_build_transitions(self):
        # need to firm up to test that this is returning the right result
        pass

class TestBallTree(unittest.TestCase):
    pass


class TestNetwork(unittest.TestCase):

    def setUp(self):
        odx = ODX(0, 1)
        odx.load_gtsf()
        day = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
        megas = odx.preprocess_gtsf(day)
        builder = NetworkBuilder(700)
        self.net = builder.build(megas, 1)

    def test_find_stop(self):
        #self.assertEqual(self.net.routes["RAIL"].stops[908480].id, 908480,msg='Object build incorrectly')
        pass

    def test_get_transition(self):
        #need to firm up test results for this itmem
        #export the ransition data to a csv to test
        #self.assertTrue(len(self.net.routes['RAIL'].trans[908480])>=1)
        self.assertTrue(max(len(x) for x in self.net.routes['RAIL'].trans.values()) > 0)
        self.net.export_transition('transition_example2.csv')
        #Test to see if two stops are mutual
        plotter = PlotStops()
        for route, stops in self.net.routes["RAIL"].trans.items():
            #plotter.add_mega(self.net.find_stop("RAIL",stop),circle=True)
            for stop, stop_list in stops.items():
                plotter.add_mega(stop,circle=True)
                for s in stop_list:
                    plotter.add_mega(s)
            break
        plotter.export('Transition_Test.html')

        #Test to see if


if __name__ == '__main__':
    unittest.main()
