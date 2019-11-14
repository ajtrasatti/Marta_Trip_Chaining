import unittest
from breeze_loader import Breeze_Loader
from apc_loader import APC_Loader
from odx import ODX
import datetime as dt
from network import NetworkBuilder
import os
import pandas as pd
from rail_mapping_loader import RailMappingLoader


class TestBreezeLoader(unittest.TestCase):

    def test_single(self):

        fileDir = os.path.realpath(__file__).split('/version_1_0')[0]
        path = os.path.join(fileDir, 'Data/breeze_test.pick')
        rail_path = os.path.join(fileDir, 'Data/RailStopsMap.csv')
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
        breeze_load = Breeze_Loader()
        df = breeze_load.load_breeze(path)
        self.assertTrue(isinstance(df, pd.DataFrame), msg="Loader works well")
        df = breeze_load.get_marta_only(df)
        self.assertTrue(df.shape[0] - df.Dev_Operator.str.contains('MARTA').sum() == 0, msg=' contains non Marta Data')
        bus, rail = breeze_load.split_frame(df)
        rail[~(rail.Dev_Operator.str.contains("Rail"))].to_csv('bad_data.csv')
        self.assertEqual(rail.shape[0] - rail.Dev_Operator.str.contains("Rail").sum(), 0, msg='Contains non rail data')
        self.assertEqual(bus.shape[0] - bus.Dev_Operator.str.contains("Bus").sum(), 0, msg='Contains non bus data')
        path = os.path.join(fileDir,'Data/RailStopsMap.csv')
        loader = RailMappingLoader()
        map_df = loader.load_rail_mappings(path)
        map_df = loader.clean_rail_mappings(map_df)
        map_df = loader.fit_2_network(map_df, net)
        path = os.path.join(fileDir, 'Data/apc_test.pick')
        apc_load = APC_Loader(net)
        apc_df = apc_load.load_apc(path)
        apc_df = apc_load.join_megas(apc_df)
        #load.match_2_apc(bus, apc_df).to_csv('apc_match_test.csv')
        bus_dict = apc_load.build_search_dict(apc_df)
        bus_df = breeze_load.apc_match(bus,bus_dict)
        bus_df.head(n=2000).to_csv('apc_breeze_test.csv')
        rail_df = breeze_load.match_rail_stops(rail, map_df)

        rail_df.head(n=100).to_csv('rail_breeze_test.csv')
        data = pd.concat([bus_df,rail_df])
        data.to_csv('Data_set_11_13.csv')
        print(data.columns)


if __name__ == '__main__':
    unittest.main()
