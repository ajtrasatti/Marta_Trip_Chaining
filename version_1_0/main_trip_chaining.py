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

    max_ind = 3
    for folder, date in zip(folders[1:max_ind], dates[1:max_ind]):
        print(date)
        temp = pd.read_csv(join(folder_path, folder, "breeze_output.csv")).drop('Unnamed: 0', axis=1)
        if breeze_df is None:
            breeze_df = temp
        else:
            breeze_df = pd.concat([breeze_df, temp])
        # print(breeze_df.tail())
    t0 = time.time()
    print("starting group"); t0 = time.time()
    groups = breeze_df.groupby("Serial_Nbr")
    print("time for grouping", time.time() - t0); t0 = time.time()

    total = len(groups)
    print(total)
    count = 0
    actual = 0
    for Serial_Nbr, df in groups:
        count += 1
        if len(df) > max_ind*5 and not np.any(df.MATCH_ERROR):
            t0 = time.time()
            actual += 1

            df.to_csv(join("../Data/People", str(Serial_Nbr) + ".csv"))
            # trip chain
            trip_chain = TripChain()
            trip_df = trip_chain.trip_chain_df(breeze_df=df, breeze_number=Serial_Nbr)
            trip_df.to_csv(join("../Data/PeopleTrips", str(Serial_Nbr) + ".csv"))

            print("COUNT IS", count, "out of", total, "actuals", actual, "time", time.time()-t0)


if __name__ == '__main__':
    main()

