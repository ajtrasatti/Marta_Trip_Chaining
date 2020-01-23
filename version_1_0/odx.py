"""
@author Joshua E. Morgan , jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
@todo Make global parameters file
@todo Output error stats to a file using an error class
"""

from os.path import join, realpath
import datetime as dt
import pandas as pd
from gtsf import GtfsFac
from apc import ApcLoader
from breeze_loader import BreezeLoader
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
        # fileDir = realpath(__file__).split('/version')[0]
        # self.data_path = join(fileDir, 'Data')
        # self.megas = None


def main():  # data, gtsf_path, ):  # day and files
    """
    :param date: used for name of folders/path
    :param gtsf_path: point to the gtsf path
    :param apc_filename: string, with time of the period that starts
    :param breeze_filename: bool, determine whether to run the function in test mode with preset parameters
    """
    import time
    t0 = time.time()

    start_day = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
    # end_day = dt.datetime.strptime("01/31/18 00:00", "%m/%d/%y %H:%M")
    # odx = ODX(start_day,end_day)

    file_dir = realpath(__file__).split('/version')[0]
    data_path = join(file_dir, "Data")
    output_path = join(file_dir, "Output")

    # GTFS

    # # gtfs_loader = GtfsLoader(join(data_path, 'gtfs'), start_day)
    # # gtfs_loader.export_megas(join(output_path, "mega_stops.csv"))  # output stops to file
    # # network = gtfs_loader.return_network()

    gtfs = GtfsFac(join(data_path, 'MARTA_gtfs'))  # @todo: probably move this one level higher
    network = gtfs.get_gtfs_network(start_day)
    # gtfs.export_megas  # @todo: export the megas that go over all the days

    # loading apc
    apc_load = ApcLoader(network)
    apc_path = join(data_path, 'apc_test.csv')
    apc_df = apc_load.load_apc(apc_path)
    # print("apc loaded", time.time() - t0)
    apc_df = apc_load.join_megas(apc_df)
    # print("joined mega on apc df", time.time() - t0)
    apc_df.to_csv(join(output_path, 'apc_output.csv'), index=False)
    print("apc complete", time.time() - t0)
    bus_dict = apc_load.build_search_dict(apc_df)

    # breeze load
    breeze_path = join(data_path, 'breeze_test.csv')  # loading breeze
    breeze_df = pd.read_csv(breeze_path, parse_dates=["Transaction_dtm"])
    breeze_load = BreezeLoader()

    # splitting the bus_df
    bus_df, rail_df = breeze_load.split_frame(breeze_df)
    print("breeze loaded", time.time() - t0)

    # Matching breeze BUS data to apc bus search dict
    bus_df = breeze_load.apc_match(bus_df, bus_dict)

    # Matching breeze RAIL data rail stops in rail_df
    path = join(data_path, 'RailStopsMap.csv')
    loader = RailMappingLoader()
    map_df = loader.load_rail_mappings(path)
    map_df = loader.clean_rail_mappings(map_df)
    map_df = loader.fit_2_network(map_df, network)
    rail_df = breeze_load.match_rail_stops(rail_df, map_df)

    df = pd.concat([bus_df, rail_df], sort=False)

    df.to_csv(join(output_path, 'breeze_output.csv'), index=False)
    print(df.head())


if __name__ == '__main__':
    main()

