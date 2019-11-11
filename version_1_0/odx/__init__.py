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
        fileDir = os.path.realpath(__file__).split('/version_1_0')[0]
        #fileDir = os.getcwd()
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

    def build_network(self, trans_limit=700,id=1):
        """

        :return:
        """
        if self.megas is not None:
            self.network = Network(self.megas, id, trans_limit)

    def preprocess_apc(self, path, start, end):
        """
        :param path: os path object file that the apc data is stored in
        :param start: dt.datetime object
        :param end: dt.datetime object
        :return: None
        """
        df = pd.read_pickle(path)
        df = df[(df['CALENDAR_ID'] >= start) & (df['CALENDAR_ID'] <= end)]
        df = df[pd.notnull(df['ARRIVAL_TM_HM'])]
        df.loc[:, "ARRIVAL_TM_HM"] = df["ARRIVAL_TM_HM"].str.split(':')
        df.insert(len(df.columns), 'ARRIVAL_DTM', df.apply(
            lambda x: x.CALENDAR_ID + dt.timedelta(hours=int(x.ARRIVAL_TM_HM[0]), minutes=int(x.ARRIVAL_TM_HM[1])),
            axis=1))
        self.apc =  df[['ROUTE_ABBR', 'SERVICE_TYPE_TEXT', 'VECHILE_TAG', 'LATITUDE', 'LONGITUDE', 'BOARD', 'ALIGHT',
                   'ARRIVAL_DTM']]

    def preprocess_breeze(self, day):
        """
        @create function to preprocess apc data
        @document
        @test
        :param day:
        :return:
        """
        self.breeze = None

    def link_data(self):
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

    def __call__(self):
        """
        This funciton
        :return:
        """
        pass