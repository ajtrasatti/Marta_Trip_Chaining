from .gtfs import GTFS
from os.path import join
import os
import datetime as dt
import bisect


class GtfsFac:
    """
    GTFS Factory - This class is used to organize many gtfs folders that span across many dates
    For any given date it will figure out which folder has the correct dates to look at
    and which service_id to look at (i.e. Weekday vs. Saturday vs. Sunday service)

    It will also manage all the stops and mega_stops to make sure that they span across all the dates consistently
        @ todo: add a stops.csv and mega_stops.csv file that can help keep track across iterations
    ex. {stop_id : {"stop_id" : stop_id, "route" : 87, "lat_lon" : [39.345,-87.3423] },
             stop_id : {...}, stop_id : {...}, ...
        }

    """
    def __init__(self, folder_path, stops_file=None, mega_stops_file=None):
        """
        :param folder_path: folder that contains (only) many folders of gtfs folders for different dates
                - folder_path (containing the following)
                    > gtfs_01_13_2018
                        >> agency.txt
                        >> calendar_dates.txt
                        >> ...
                    > gtfs_01_30_2018
                        >> ...
                    > gtfs_mm_dd_YYYY
                        >> ...
                    > ...
        :param stops_file: will be added so that mega stop names stay consistent over time (file can be appended)
        :param mega_stops_file:  will be added so that mega stop names stay consistent over time (file can be appended)
        """

        self.folders = [name for name in os.listdir(folder_path) if os.path.isdir(join(folder_path,name))]  # list of folders in directory

        to_dt = lambda folder_name: dt.datetime(int(folder_name[-4:]), int(folder_name[-10:-8]), int(folder_name[-7:-5]))
        self.dates = sorted([to_dt(name) for name in self.folders])  # ex. gtfs_mm_dd_YYYY
        print(self.dates)
        self.gtfs_dict = {}
        self.stops = {}
        self.megas = {}  # or []??

        for folder, date in zip(self.folders, self.dates):
            self.gtfs_dict[date] = GTFS(join(folder_path, folder), date)

            # self.stops = ??
            # self.megas = append??

    def get_gtfs_network(self, date):
        ind = bisect.bisect_right(self.dates, date) - 1  # find index of last date that the gtfs data was updated
        print(self.dates, date)
        print("ind", ind)
        ind_date = self.dates[ind]  # get the date to use as index for gtfs dictionary
        print("date, ind_date", ind_date, date)
        return self.gtfs_dict[ind_date].get_network(date)

    def get_gtfs_routes_dict(self,date):
        return self.get_gtfs_network(date).routes_dict

    def get_megas(self):
        return self.megas

    def export_megas(self, filename, date):
        self.gtfs_dict[date].export_megas(filename, date)



