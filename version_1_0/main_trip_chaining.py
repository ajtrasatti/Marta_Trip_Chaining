"""
@author Anthony J. Trasatti , atrasatti3@gatech.edu
Socially Aware Mobility (SAM) Lab, Georgia Tech
v_1.0
"""

import os
from os.path import join, realpath
import datetime as dt
import numpy as np
import pandas as pd
from trip_chaining import TripChain
import csv

def main():
    import time
    t0 = time.time()

    file_dir = realpath(__file__).split('/version')[0]
    my_path = join(file_dir, "Data")
    folder_path = join(my_path, "partitioned")

    def to_dt(folder):  # This is for the specific folder format that is being used
        x = folder.split("_")
        return dt.datetime(int(x[0]), int(x[1]), int(x[2]))
    # list of folders in directory
    folders = [name for name in os.listdir(folder_path) if os.path.isdir(join(folder_path, name))]
    dates, folders = zip(*sorted([(to_dt(folder), folder) for folder in folders]))

    breeze_df = None

    start_ind = 91
    max_ind = 10
    for folder, date in zip(folders[start_ind:start_ind+max_ind], dates[start_ind:start_ind+max_ind]):
        print(date)
        temp = pd.read_csv(join(folder_path, folder, "breeze_output.csv")).drop('Unnamed: 0', axis=1)
        if breeze_df is None:
            breeze_df = temp
        else:
            breeze_df = pd.concat([breeze_df, temp])
        # print(breeze_df.tail())
    t0 = time.time()
    print("starting group"); t0 = time.time()
    breeze_df.Transaction_dtm = pd.to_datetime(breeze_df.Transaction_dtm)
    groups = breeze_df.groupby("Serial_Nbr")
    print("time for grouping", time.time() - t0); t0 = time.time()

    total = len(groups)
    print(total)
    count = -1
    # actual = 0

    filename = join("../Data", "trips_test.csv")
    csv_file = open(filename, 'w')
    csv_writer = csv.writer(csv_file)

    header = ["trip_id", "breeze_id", "start_stop", "start_time", "end_stop", "end_time",
                         "stops", "routes", "num_legs", "used_bus", "used_train", "error_bool", "error_details"]
    csv_writer.writerow(header)

    t0 = time.time()
    t2 = time.time()
    t4 = 0

    for Serial_Nbr, df in groups:
        count += 1
        # if len(df) > max_ind*5 and not np.any(df.MATCH_ERROR):

        # df.to_csv(join("../Data/People", str(Serial_Nbr) + ".csv"))
        # if count == 2000:  # early cut off
        #     break

        # trip chain

        trip_chain = TripChain()
        if count % 1000 == 0:
            t1 = t2
            t2 = time.time()
            t3 = t4
            t4 = 0
            verbose = True
        else:
            verbose = False

        # @todo - test how the time is distributed here for chaining vs appending
        trip_df = trip_chain.trip_chain_df(breeze_df=df, breeze_number=Serial_Nbr, verbose=verbose)

        csv_writer.writerows(trip_df.values)

        # if trips_df is None:
        #     print("TEST TEST ")
        #     trips_df = trip_df
        # else:
        #     temp_time = time.time()
        #     trips_df = trips_df.append(trip_df)
        #     t4 += time.time() - temp_time

        
        if verbose:
            print("COUNT IS", count, "out of", total, "time", time.time()-t0, "time for 1000", time.time()-t1, "append time", t3)

    # csv_writer.writerowss(trips_df.values)
    # trips_df.to_csv(join("../Data", "trips.csv"))


if __name__ == '__main__':
    main()

