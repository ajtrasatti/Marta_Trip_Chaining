"""
@author Anthony J. Trasatti , atrasatti3@gatech.edu
@author Joshua E. Morgan , jmorgan63@gatech.edu
Socially Aware Mobility (SAM) Lab, Georgia Tech
v_1.0
"""


class Stop:
    """
    Stop class represents a stop in the MARTA gtfs data
    Attributes
        - stop_id - int, unique identifier for a stop
        - lat - latitude value for a given stop
        - lon - longitude value for a given stop
    """
    def __init__(self, stop_id, lat, lon):
        self.stop_id = stop_id  # stop_id number from gtfs
        # self.dev_op = dev_op  # in case you use gtfs from multiple areas with overlapping stop_ids
        self.lat = lat
        self.lon = lon
        # self.tran = {}  # dict {route_id : [Stops]} contains routes pointed to MegaStops that are valid transitions

    def __eq__(self, other):
        return self.stop_id == other.stop_id

    def __ge__(self, other):
        return self.stop_id >= other.stop_id

    def __lt__(self, other):
        return self.stop_id < other.stop_id

    def __hash__(self):
        return hash(self.stop_id)

    def __str__(self):
        return (
            f"Stop("
            f"stop_id={self.stop_id},"
            f"lat={self.lat:.5f},"
            f"lon={self.lon:.5f})"
        )

    def get_lat_lon(self):
        return self.lat, self.lon

    def to_tuple(self):
        return self.stop_id, self.lat, self.lon

    # def get_tran(self, route_id):
    #     return self.tran[route_id]

#
# class BusStop(Stop):
#
#     def __init__(self, id, lat, lon):
#         super(BusStop, self).__init__(id,lat,lon)
#
#     def to_tuple(self):
#         return ('Bus', self.id, self.lat, self.lon)
#
#
# class TrainStop(Stop):
#     def __init__(self, id, lat, lon, lines):
#         super(TrainStop, self).__init__(id, lat, lon)
#         self.lines = lines
#
#     def __str__(self):
#         return f"Train Stop: {self.id}"
#
#     def to_tuple(self):
#         return ('Train', self.id, self.lat, self.lon, ";".join(line for line in self.lines))
#
#
# class MegaStop(Stop):
#
#     def __init__(self, id, stops, avg= False):
#         super(MegaStop, self).__init__(id, stops[0].lat, stops[0].lon)
#         self.stops = stops
#         if avg:
#             self.lat = sum(stop.lat for stop in self.stops) / len(self.stops)
#             self.lon = sum(stop.lon for stop in self.stops) / len(self.stops)
#
#     def __str__(self):
#         return f"Mega Stop: {self.id}"
#
#     def to_csv(self, route_id):
#         """
#         This extracts all of the stops belonging too the mega stops
#         :param route_id: string
#         :return: list of stop tuples
#         """
#         return [(route_id, stop.id, stop.lat, stop.lon, self.id, self.lat, self.lon) for stop in self.stops]
#         # if route:
#         #     return ([(self.id, stop.id, self.lat, self.lon, stop.lat, stop.lon,route)
#         #              for stop in self.stops for route in self.routes])
#         # else:
#         #     return [(self.id, stop.id,self.lat,self.lon,stop.lat,stop.lon) for stop in self.stops]
#
#     def to_json(self):
#         """
#
#         :return:
#         """
#         pass
