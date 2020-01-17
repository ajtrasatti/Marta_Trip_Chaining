import pandas as pd
from os.path import join
from .schedule import ScheduleMaker
from .mega_stop_fac import MegaStopFac
from .network import NetworkBuilder
from .RailStopFac import RailStopFac

##############################
# Global Parameters
global MAX_DIST
MAX_DIST = 700  # max distance between stops

class GTFS_Loader:
    def __init__(self, gtfs_path, start):
        self.gtfs = self.load_gtfs(gtfs_path)  # loading gtfs
        self.scheduler = ScheduleMaker(self.gtfs['trips'], self.gtfs['calendar'],
                                       self.gtfs['stop_times'], self.gtfs['stops'], self.gtfs['routes'])

        self.megas = self.preprocess_gtfs(start)  # preprocessing gtfs data
        self.network = NetworkBuilder(MAX_DIST).build(self.megas, id)  # builidng a network

    def load_gtfs(self ,gtfs_path):
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
        return {"trips": trips, 'stops': stops, "stop_times": stop_times, "routes": routes, 'calendar': cal}

    def preprocess_gtfs(self, day):
        """
        @document
        :param day:
        :return:
        """
        self.scheduler.build_daily_table(day)
        routes, train_dict = self.scheduler.get_routes()
        route_ms = {}
        MSF = MegaStopFac(MAX_DIST)
        for route in routes.keys():
            route_ms[route] = MSF.get_mega_stops(routes[route][0] ,routes[route][1])

        rsf = RailStopFac(MAX_DIST, MSF.count) # @ TODO: put this into mega stop factory
        route_ms["RAIL"] = rsf.get_rail_stops(train_dict)

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
            writer.writerow(["ROUTE",'STOP_ID',"LAT","LON",'MEGA_STOP_ID',"mega_LAT","mega_LON"])
            for route, mega in self.megas.items():
                for stop in mega:
                    writer.writerows(list(stop.to_csv(route)))

    def return_network(self):
        return self.network