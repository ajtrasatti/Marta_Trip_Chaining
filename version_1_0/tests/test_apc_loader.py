import unittest
import pandas as pd
import apc_loader
import os
from odx import ODX
import datetime as dt
from network import NetworkBuilder

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
        print(load.join_megas(df).head())

    def test_muliple(self):
        pass





if __name__ == '__main__':
    unittest.main()
