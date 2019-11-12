import unittest
import pandas as pd
import apc_loader
import os
from odx import ODX
import datetime as dt
from network import NetworkBuilder
import random

class TestAPCLoader(unittest.TestCase):


    def test_single(self):
        odx = ODX(0, 1)
        odx.load_gtsf()
        day = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
        self.megas = odx.preprocess_gtsf(day)
        builder = NetworkBuilder(700)
        net = builder.build(self.megas, 1)
        fileDir = os.path.realpath(__file__).split('/version_1_0')[0]
        path = os.path.join(fileDir, 'Data/apc_test.pick')
        load = apc_loader.APC_Loader(net)
        df = load.load_apc(path)
        self.assertTrue(isinstance(load.load_apc(path),pd.DataFrame), msg="Loader works well")
        self.assertTrue(type(load.get_route_tree('19')) != int, msg='Network stored as int works incorrectly')
        self.assertTrue(type(load.get_route_tree(19)) == int, msg='Test works incorrectly')
        self.assertTrue(load.join_megas(df,True) == 0)
        _ = load.join_megas(df)
        print(_)
        _.to_csv('apc_test_w_ms.csv')
        print(load.build_bus_tree(df))

    def test_muliple(self):
        pass


class TestBusTree(unittest.TestCase):

    def setUp(self):
        self.times = [dt.datetime(year=2018, month=1, day=30, hour=random.randint(0, 23), minute=random.randint(0, 59)) for i
                 in range(10)]
        self.stops = [i for i in range(10)]
        self.routes = [i % 2 for i in range(10)]


    def test_time_index(self):
        """

        :return:
        """
        tree = apc_loader.BusTree(self.stops,self.routes,self.times)
        self.times = sorted(self.times)
        _ = tree.find_time_index(self.times[0])
        self.assertEqual(0,_-1)
        _ = tree.find_time_index(self.times[9])
        self.assertEqual(9,_-1)
        _ = tree.find_time_index(self.times[5])
        self.assertEqual(5,_-1)

    def test_stop_indexs(self):
        """

        :return:
        """
        tree = apc_loader.BusTree(self.stops,self.routes,self.times)
        times = sorted([(i,t) for i,t in enumerate(self.times)],key = lambda x:x[1])
        _ = tree.find_stop_route(times[0][1])
        self.assertEqual(_[1],self.stops[times[0][0]], msg="First Edge case")
        _ = tree.find_stop_route(times[5][1])
        self.assertEqual(_[1],self.stops[times[5][0]],msg='Middle Case')
        _ = tree.find_stop_route(times[9][1])
        self.assertEqual(_[1],self.stops[times[9][0]],msg='End Edge Case')
        t1 = times[1][1]
        t2 = times[2][1]
        delta_t = (t2 - t1).seconds / 2
        _ = tree.find_stop_route(t1 + dt.timedelta(seconds =delta_t))
        self.assertEqual(self.stops[times[1][0]],_[1], msg="In Between Numbers case")
        _ = tree.find_stop_route(t1 + dt.timedelta(seconds=delta_t-1))
        self.assertEqual(self.stops[times[1][0]], _[1],msg="Lower Numbers case")
        _ = tree.find_stop_route(t1 + dt.timedelta(seconds=delta_t + 1))
        self.assertEqual( self.stops[times[2][0]],_[1], msg="Upper Numbers case")




if __name__ == '__main__':
    unittest.main()
