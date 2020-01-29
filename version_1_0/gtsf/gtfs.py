import pandas as pd
from os.path import join
from .schedule import ScheduleMaker
from .mega_stop_fac import MegaStopFac
from .network import Network
from .RailStopFac import RailStopFac

##############################
# Global Parameters
global MAX_DIST
MAX_DIST = 700  # max distance between stops


def load_gtfs(gtfs_path):
    """
    build the gtsf dict of pandas dfs

    :param gtfs_path: path to the gtfs
    :return: gtfs: a dictionary of keys (strings) with values (Pandas DataFrames)
    """
    trips = pd.read_csv(join(gtfs_path, 'trips.txt'))
    stops = pd.read_csv(join(gtfs_path, 'stops.txt'))
    stop_times = pd.read_csv(join(gtfs_path, "stop_times.txt"))
    routes = pd.read_csv(join(gtfs_path, 'routes.txt'))
    cal = pd.read_csv(join(gtfs_path, 'calendar.txt'))
    gtfs = {"trips": trips, 'stops': stops, "stop_times": stop_times, "routes": routes, 'calendar': cal}
    return gtfs


class GTFS:
    def __init__(self, gtfs_path, start, megas=None):  # @todo : make megas shared among the GTFS's
        self.start_date = start
        self.gtfs = load_gtfs(gtfs_path)  # loading gtfs
        self.network = {}
        self.route_mega_dict = {}
        self.scheduler = {}

        for service_id in [3, 4, 5]:  # automatically figure out possible service ids ?
            self.scheduler[service_id] = ScheduleMaker(self.gtfs['trips'], self.gtfs['stop_times'], self.gtfs['stops'],
                                                       self.gtfs['routes'], service_id)
            routes_dict, train_dict = self.scheduler[service_id].get_routes()

            # @todo - make these not part of init
            self.route_mega_dict[service_id] = self.build_mega_dict(routes_dict, train_dict)
            self.network[service_id] = Network(self.route_mega_dict[service_id], MAX_DIST, service_id)

    def get_service_id(self, date):
        """
        Finds the specific service type for a given day
        :param day: dt.DateTime object containing the date of the rest
        :return: int, the service type of the

        """
        day_o_week = date.weekday()
        for tup in self.gtfs['calendar'].itertuples():
            if tup[day_o_week + 2] == 1:
                service_id = tup.service_id

            # @ TODO add exceptions for calendar_dates.txt
            # if excption
                # return exception service_id
            # else
                return service_id

    # def build_mega_dict(self, routes_dict, train_dict):
    #     """
    #     @document
    #     :param routes_dict: # dict {route_id : [mega_ids]}
    #     :param train_dict:
    #     :return: dict {route_id : [MegaStops]}
    #     """
    #     route_mega_dict = {}
    #     MSF = MegaStopFac(MAX_DIST)
    #     for route in routes_dict.keys():
    #         route_mega_dict[route] = MSF.get_mega_stops(routes_dict[route][0], routes_dict[route][1]) # this makes a route??
    #
    #     rsf = RailStopFac(MAX_DIST, MSF.count)  # @ TODO: put this into mega stop factory
    #     route_mega_dict["RAIL"] = rsf.get_rail_stops(train_dict)
    #
    #     return route_mega_dict  # dict {route_id : [MegaStops]}

    def export_megas(self, path_out, date):
        """
        This file exports the megastops to a specific file for analysis
        :param path_out:
        :return:
        """

        with open(path_out, 'w') as fout:
            import csv
            writer = csv.writer(fout)
            writer.writerow(["ROUTE", "STOP_ID", "LAT", "LON",
                             "MEGA_STOP_ID", "mega_LAT", "mega_LON"])
            service_id = self.get_service_id(date)
            for route, mega in self.route_mega_dict[service_id].items():
                for stop in mega:
                    writer.writerows(list(stop.to_csv(route)))

    def get_network(self, date):
        service_id = self.get_service_id(date)
        return self.network[service_id]
