"""
@author Joshua E. Morgan , jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
@todo cleanup and reimplement main method to use the odx class functions
@todo provide more parameters to be enetered in the odx init statement to tune system
@todo set up object that can store the error stats from different processes
"""

from os.path import join, realpath
import datetime as dt
import pandas as pd

from gtsf import GTFS_Loader

from apc import APC_Loader
from breeze_loader import Breeze_Loader
from rail_mapping_loader import RailMappingLoader


class ODX:
    """
    This is the odx class which has the main
    Attributes
        - start -
        - end -
        - test
        -
    """
    def __init__(self, start, end, test=True, **kwargs):
        """

        :param start: string, with time of the period that starts
        :param end: string, with time of the period that starts
        :param test: bool, determine wether to run the function in test mode with preset parameters
        :param kwargs:
        """
        fileDir = realpath(__file__).split('/version')[0]
        self.data_path = join(fileDir, 'Data')
        self.megas = None

def main(): # day and files
    import time
    t0 = time.time()

    start_day = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
    # end_day = dt.datetime.strptime("01/31/18 00:00", "%m/%d/%y %H:%M")
    # odx = ODX(start_day,end_day)

    fileDir = realpath(__file__).split('/version')[0]
    data_path = join(fileDir,"Data")
    output_path  = join(fileDir,"Output")

    # GTSF
    gtfs_loader = GTFS_Loader(join(data_path, 'gtfs'), start_day)
    gtfs_loader.export_megas(join(output_path, "megastops.csv")) # output stops to file
    network = gtfs_loader.return_network() # @ to_do - return network depending on day

    # loading apc
    apc_load = APC_Loader(network)
    apc_path = join(data_path, 'apc_test.csv')
    apc_df = apc_load.load_apc(apc_path)
    apc_df = apc_load.join_megas(apc_df)
    apc_df.to_csv(join(output_path, 'apc_output.csv'), index=False)

    print("apc loaded", time.time() - t0)
    bus_dict = apc_load.build_search_dict(apc_df)


    # breeze load
    breeze_path = join(data_path, 'breeze_test.csv') # loading breeze
    breeze_df = pd.read_csv(breeze_path,parse_dates=["Transaction_dtm"])
    breeze_load = Breeze_Loader()
    # splitting the bus_df
    bus_df, rail_df = breeze_load.split_frame(breeze_df)
    print("breeze loaded", time.time() - t0)



    bus_df = breeze_load.apc_match(bus_df, bus_dict) # breeze to apc, match

    path = join(data_path, 'RailStopsMap.csv')

    loader = RailMappingLoader()
    map_df = loader.load_rail_mappings(path)
    map_df = loader.clean_rail_mappings(map_df)
    map_df = loader.fit_2_network(map_df, network)
    rail_df = breeze_load.match_rail_stops(rail_df, map_df)

    df = pd.concat([bus_df, rail_df],sort=False)



    df.to_csv(join(output_path,'breeze_output.csv'), index=False)
    print(df.head())

if __name__ == '__main__':
    main()

