"""
@author Joshua E. Morgan , jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
"""
import os
import datetime as dt
import pandas as pd
import schedule
from mega_stop_fac import MegaStopFac
from network import Network
from Rail_stop_fac import RailStopFac

class ODX:
    """
    This is the odx class which has the main

    """
    def __init__(self, start, end, **kwargs):
        """

        :param start: string, with time of the period that starts
        :param end: string, with time of the period that starts
        :param kwargs:
        """
        self.start = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
        self.end = dt.datetime.strptime("01/31/18 00:00", "%m/%d/%y %H:%M")
        fileDir = os.path.realpath('__file__').split('/code')[0]
        self.data_path = os.path.join(fileDir, 'Data')
        self.megas = None

    def load_gtsf(self):
        """
        build a documents search tree for this so we can get the correct days data
        function loads all of the gtsf tables Exclusively
        :param gtsf_path: path to the gtsf
        :return:
        """
        gtsf_path = os.path.join(self.data_path, 'gtsf')
        trips = pd.read_csv(os.path.join(gtsf_path, 'trips.txt'))
        stops = pd.read_csv(os.path.join(gtsf_path, 'stops.txt'))
        stop_times = pd.read_csv(os.path.join(gtsf_path, "stop_times.txt"))
        routes = pd.read_csv(os.path.join(gtsf_path, 'routes.txt'))
        cal = pd.read_csv(os.path.join(gtsf_path, 'calendar.txt'))
        self.gtsf = {"trips": trips, 'stops': stops, "stop_times": stop_times, "routes": routes, 'calendar': cal}

    def load_apc(self, apc_path):
        """
        Need to build a script to break these apart and store in seperate data buckets.
        Need to implement the search tree to find the given file containing the precompiled daily data
        @document apc function
        @test functionality
        :param apc_path:
        :return:
        """
        self.apc = pd.read_pickle(os.path.join(self.data_path, 'apc.pick'))

    def load_breeze(self, breeze_path):
        """
        Need to build a script to break these apart and store in seperate data buckets.
        Need to implement the search tree to find the given file containing the precompiled daily data
        @document breeze function
        @test functionality
        :param breeze_path:
        :return:
        """
        self.breeze = pd.read_pickle(os.path.join(self.data_path, 'breeze.pick'))

    def preprocess_gtsf(self, day):
        """
        @document
        :param day:
        :return:
        """
        self.MegaStopFactory = MegaStopFac(700)
        self.scheduler = schedule.ScheduleMaker(self.gtsf['trips'],self.gtsf['calendar'],
                              self.gtsf['stop_times'],self.gtsf['stops'],self.gtsf['routes'])
        self.scheduler.build_daily_table(day)
        routes, train_dict = self.scheduler.get_routes()
        route_ms = {}
        for route in routes.keys():
            _ = self.MegaStopFactory.get_mega_stops(routes[route][0],routes[route][1])
            route_ms[route] = _
        rsf = RailStopFac(700,self.MegaStopFactory.count)
        route_ms["RAIL"] = rsf.get_rail_stops(train_dict)
        self.megas = route_ms
        return route_ms

    def export_megas(self, path_out):
        """
        This file exports the megastops to a specific file for analysis
        :param path_out:
        :return:
        """
        with open(path_out, 'w') as fout:
            import csv
            writer = csv.writer(fout)
            writer.writerow(["ROUTE",'MEGA_STOP_ID',"LAT","LON"])
            for route, mega in self.megas.items():
                for stop in mega:
                    writer.writerow([route]+ list(stop.to_csv()))

    def build_network(self, trans_limit,id=1):
        """

        :return:
        """
        if self.megas is not None:
            self.network = Network(self.megas, id, 700)


    def preprocess_apc(self, day):
        """
        @create function to preprocess apc data
        @document
        @test
        :param day:
        :return:
        """
        pass

    def preprocess_breeze(self, day):
        """
        @create function to preprocess apc data
        @document
        @test
        :param day:
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

    def __call__(self):
        """
        This funciton
        :return:
        """
        pass