"""
@author Anthony J. Trasatti , atrasatti3@gatech.edu
@author Joshua E. Morgan , jmorgan63@gatech.edu
Socially Aware Mobility (SAM) Lab, Georgia Tech
v_1.0
@todo Output error stats to a file using an error class
"""

import os
from os.path import join, realpath
import datetime as dt
import pandas as pd

from gtsf import GtfsFac
from apc import APC
from breeze_loader import BreezeLoader
from rail_mapping_loader import RailMappingLoader


def trip_chaining(gtfs, day, data_path, rail_path):  # data, gtsf_path, ):  # day and files
    """
    :param gtfs: GTFS Factory object
    :param day: date_time object
    :param data_path: folder that contains apc_test.csv, breeze.csv
    :param rail_path: folder that contains apc_test.csv, breeze.csv
    """
    import time
    t0 = time.time()

    routes_dict = gtfs.get_gtfs_routes_dict(day)
    # print("got_routes_dict", time.time() - t0)

    # loading apc
    apc_file = join(data_path, 'apc_test.csv')
    apc = APC(apc_file)
    apc.join_megas(routes_dict)
    # print("megas joined on apc", time.time() - t0)
    apc.export_apc_df(join(data_path, 'apc_output.csv'))
    bus_search_dict = apc.get_bus_search_dict()

    # breeze load
    breeze_path = join(data_path, 'breeze_test.csv')  # loading breeze
    breeze_df = pd.read_csv(breeze_path, parse_dates=["Transaction_dtm"])
    breeze_load = BreezeLoader()

    # splitting the bus_df
    bus_df, rail_df = breeze_load.split_frame(breeze_df)
    # print("breeze loaded", time.time() - t0)

    # Matching breeze BUS data to apc bus search dict
    bus_df = breeze_load.apc_match(bus_df, bus_search_dict)

    # Matching breeze RAIL data rail stops in rail_df
    rail_loader = RailMappingLoader()
    rail_mapping = rail_loader.load_rail_mappings(rail_path)
    rail_mapping = rail_loader.clean_rail_mappings(rail_mapping)
    rail_mapping = rail_loader.fit_2_network(rail_mapping, routes_dict)

    rail_df = breeze_load.match_rail_stops(rail_df, rail_mapping)

    df = pd.concat([bus_df, rail_df], sort=False)

    df.to_csv(join(data_path, 'breeze_output.csv'), index=False)
    print(df.head())


def main():
    import time
    t0 = time.time()
    file_dir = realpath(__file__).split('/version')[0]
    my_path = join(file_dir, "Data")
    folder_path = join(my_path, "partitioned")
    # list of folders in directory

    def to_dt(folder):  # This is for the specific folder format that is being used
        x = folder.split("_")
        return dt.datetime(int(x[0]), int(x[1]), int(x[2]))
    folders = [name for name in os.listdir(folder_path) if os.path.isdir(join(folder_path, name))]
    dates = sorted([to_dt(folder) for folder in folders])
    # print(dates[90])

    rail_path = join(my_path, 'RailStopsMap.csv')
    gtfs = GtfsFac(join(my_path, 'MARTA_gtfs'))
    # print("made_gtsf", time.time() - t0) # about 30 secs
    print("GTFS made", time.time()-t0)

    # for date in dates[0:90]:  # @todo : remove this to run all
    for date in dates:
        t0 = time.time()
        print("Processing ", date)
        data_path = join(my_path, "partitioned", str(date.year) + "_" + str(date.month) + "_" + str(date.day))
        trip_chaining(gtfs, date, data_path, rail_path)
        print("Processed", date, time.time() - t0)


if __name__ == '__main__':
    main()
