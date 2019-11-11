import unittest
from breeze_loader import Breeze_Loader
from apc_loader import APC_Loader
from odx import ODX
import datetime as dt
from network import NetworkBuilder
import os
import pandas as pd


class TestBreezeLoader(unittest.TestCase):

    def test_single(self):

        fileDir = os.path.realpath(__file__).split('/version_1_0')[0]
        path = os.path.join(fileDir, 'Data/breeze_test.pick')
        load = Breeze_Loader()
        df = load.load_breeze(path)
        self.assertTrue(isinstance(df, pd.DataFrame), msg="Loader works well")
        df = load.get_marta_only(df)
        self.assertTrue(df.shape[0] - df.Dev_Operator.str.contains('MARTA').sum() == 0, msg=' contains non Marta Data')
        bus, rail = load.split_frame(df)
        rail[~(rail.Dev_Operator.str.contains("Rail"))].to_csv('bad_data.csv')
        self.assertEqual(rail.shape[0] - rail.Dev_Operator.str.contains("Rail").sum(), 0, msg='Contains non rail data')
        self.assertEqual(bus.shape[0] - bus.Dev_Operator.str.contains("Bus").sum(),0, msg='Contains non bus data')


    def test_with_apc(self):
        odx = ODX(0, 1)
        odx.load_gtsf()
        day = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
        self.megas = odx.preprocess_gtsf(day)
        builder = NetworkBuilder(700)
        net = builder.build(self.megas, 1)
        fileDir = os.path.realpath(__file__).split('/version_1_0')[0]
        path = os.path.join(fileDir, 'Data/breeze_test.pick')
        load = Breeze_Loader()
        df = load.load_breeze(path)
        self.assertTrue(isinstance(df, pd.DataFrame), msg="Loader works well")
        df = load.get_marta_only(df)
        self.assertTrue(df.shape[0] - df.Dev_Operator.str.contains('MARTA').sum() == 0, msg=' contains non Marta Data')
        bus, rail = load.split_frame(df)
        rail[~(rail.Dev_Operator.str.contains("Rail"))].to_csv('bad_data.csv')
        self.assertEqual(rail.shape[0] - rail.Dev_Operator.str.contains("Rail").sum(), 0, msg='Contains non rail data')
        self.assertEqual(bus.shape[0] - bus.Dev_Operator.str.contains("Bus").sum(), 0, msg='Contains non bus data')
        path = os.path.join(fileDir, 'Data/apc_test.pick')
        apc_load = APC_Loader(net)
        apc_df = apc_load.load_apc(path)
        apc_df = apc_load.join_megas(apc_df)
        #load.match_2_apc(bus, apc_df).head(n=50).to_csv('match_test.csv')
        

if __name__ == '__main__':
    unittest.main()
