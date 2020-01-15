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
import schedule
from mega_stop_fac import MegaStopFac
from network import NetworkBuilder
from RailStopFac import RailStopFac
from apc import APC_Loader
from breeze_loader import Breeze_Loader
from rail_mapping_loader import RailMappingLoader



global MAX_DIST
MAX_DIST = 700  # max distance between stops

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
        # if test:
        #     self.start = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
        #     self.end = dt.datetime.strptime("01/31/18 00:00", "%m/%d/%y %H:%M")
        # else:
        #     self.start = start
        #     self.end = end


    def load_gtfs(self,gtfs_path):
        """
        build a documents search tree for this so we can get the correct days data
        function loads all of the gtfs tables Exclusively
        :param gtfs_path: path to the gtfs
        :return:
        """
        trips = pd.read_csv(join(gtfs_path, 'trips.txt'))
        stops = pd.read_csv(join(gtfs_path, 'stops.txt'))
        stop_times = pd.read_csv(join(gtfs_path, "stop_times.txt"))
        routes = pd.read_csv(join(gtfs_path, 'routes.txt'))
        cal = pd.read_csv(join(gtfs_path, 'calendar.txt'))
        self.gtfs = {"trips": trips, 'stops': stops, "stop_times": stop_times, "routes": routes, 'calendar': cal}

    def preprocess_gtfs(self, day):
        """
        @document
        :param day:
        :return:
        """
        self.MegaStopFactory = MegaStopFac(MAX_DIST)
        self.scheduler = schedule.ScheduleMaker(self.gtfs['trips'],self.gtfs['calendar'],
                              self.gtfs['stop_times'],self.gtfs['stops'],self.gtfs['routes'])
        self.scheduler.build_daily_table(day)
        routes, train_dict = self.scheduler.get_routes()
        route_ms = {}
        for route in routes.keys():
            _ = self.MegaStopFactory.get_mega_stops(routes[route][0],routes[route][1])
            route_ms[route] = _
        rsf = RailStopFac(MAX_DIST,self.MegaStopFactory.count)
        route_ms["RAIL"] = rsf.get_rail_stops(train_dict)
        self.megas = route_ms
        return route_ms

    def load_apc(self, apc_path):
        """
        Need to build a script to break these apart and store in seperate data buckets.
        Need to implement the search tree to find the given file containing the precompiled daily data
        :param apc_path: path for the apc_data
        :return:
        """
        self.apc = pd.read_pickle(join(self.data_path, 'apc.csv'))

    def load_breeze(self, breeze_path):
        """
        Need to build a script to break these apart and store in seperate data buckets.
        Need to implement the search tree to find the given file containing the precompiled daily data
        @document breeze function
        @test functionality
        :param breeze_path:
        :return:
        """
        self.breeze = pd.read_pickle(join(self.data_path, 'breeze.csv'))



    def export_megas(self, path_out):
        """
        This file exports the megastops to a specific file for analysis
        :param path_out:
        :return:
        """
        with open(path_out, 'w') as fout:
            import csv
            writer = csv.writer(fout)
            writer.writerow(["ROUTE",'STOP_ID',"LAT","LON",'MEGA_STOP_ID',"mega_LAT","mega_LON"])
            for route, mega in self.megas.items():
                for stop in mega:
                    writer.writerows(list(stop.to_csv(route)))

    def build_network(self, trans_limit=MAX_DIST,id = 1):
        """

        :return:
        """
        if self.megas is not None:
            builder = NetworkBuilder(trans_limit)
            self.network = builder.build(self.megas, id)

    # def preprocess_apc(self, path, start, end):
    #     """
    #     :param path: os path object file that the apc data is stored in
    #     :param start: dt.datetime object
    #     :param end: dt.datetime object
    #     :return: None
    #     """
    #     apc_load = APC_Loader(self.network)
    #     apc_df = apc_load.load_apc(path)
    #     apc_df = apc_load.join_megas(apc_df)
    #     return apc_df
    #
    #
    # def preprocess_breeze(self, path):
    #     """
    #     :param path:
    #     :return:
    #     """
    #     breeze_load = Breeze_Loader()
    #     breeze_df = breeze_load.load_breeze(path)
    #     bus_df, rail_df = breeze_load.split_frame(breeze_df)
    #     return bus_df, rail_df

    def link_rail_data(self, rail_df, data_path):
        """

        :param rail_mappings:
        :param rail_df:
        :return:
        """
        pass


    def link_data(self, bus_df, rail_df):
        """

        :return:
        """
        pass



    def trip_chain(self):
        """
        @create function to preprocess apc data
        @document
        @test
        :return:
        """
        pass

def main(): # day and files
    import time
    t0 = time.time()

    start = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
    end = dt.datetime.strptime("01/31/18 00:00", "%m/%d/%y %H:%M")
    odx = ODX(start,end)

    fileDir = realpath(__file__).split('/version')[0]
    data_path = join(fileDir,"Data")
    output_path  = join(fileDir,"Output")


    odx.load_gtfs(join(data_path, 'gtfs')) # loading gtfs
    odx.preprocess_gtfs(start) # preprocessing gtfs data
    odx.build_network(MAX_DIST) # builidng a network
    odx.export_megas(join(output_path, "megastops.csv"))


    # loading apc
    apc_load = APC_Loader(odx.network)
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
    map_df = loader.fit_2_network(map_df, odx.network)
    rail_df = breeze_load.match_rail_stops(rail_df, map_df)

    df = pd.concat([bus_df, rail_df],sort=False)



    df.to_csv(join(output_path,'breeze_output.csv'), index=False)
    print(df.head())

if __name__ == '__main__':
    main()

