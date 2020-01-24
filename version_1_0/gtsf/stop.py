"""
@author Joshua E. Morgan , jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
"""

class Stop:
    """
    Stop class represents a stop in the MARTA gtfs data
    Attributes
        - id - int, unique identifier for a stop
        - lat - lattitude value for a given stop
        - lon - longitude value for a given stop
    """
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.tran = {}  # dict {route_id : [MegaStop]} contains routes pointed to MegaStops that are valid transitions

    def __eq__(self, other):
        return self.id == other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __lt__(self,other):
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return (
            f"Stop Object"
            f"id = {self.id}"
            f"lat = {self.lat}"
            f"lon = {self.lon}"
        )

    def get_tran(self, route_id):
        return self.tran[route_id]

    def to_tuple(self):
        return (self.id, self.lat, self.lon)


class BusStop(Stop):

    def __init__(self,id, lat, lon):
        super(BusStop, self).__init__(id,lat,lon)

    def to_tuple(self):
        return ('Bus', self.id, self.lat, self.lon)


class TrainStop(Stop):
    def __init__(self, id, lat, lon, lines):
        super(TrainStop, self).__init__(id, lat, lon)
        self.lines = lines

    def __str__(self):
        return f"Train Stop: {self.id}"

    def to_tuple(self):
        return ('Train', self.id, self.lat, self.lon, ";".join(line for line in self.lines))


class MegaStop(Stop):

    def __init__(self, id, stops, avg= False):
        super(MegaStop, self).__init__(id, stops[0].lat, stops[0].lon)
        self.stops = stops
        if avg:
            self.lat = sum(stop.lat for stop in self.stops) / len(self.stops)
            self.lon = sum(stop.lon for stop in self.stops) / len(self.stops)

    def __str__(self):
        return f"Mega Stop: {self.id}"

    def to_csv(self, route_id):
        """
        This extracts all of the stops belonging too the mega stops
        :param route_id: string
        :return: list of stop tuples
        """
        return [(route_id, stop.id, stop.lat, stop.lon, self.id, self.lat, self.lon) for stop in self.stops]
        # if route:
        #     return ([(self.id, stop.id, self.lat, self.lon, stop.lat, stop.lon,route)
        #              for stop in self.stops for route in self.routes])
        # else:
        #     return [(self.id, stop.id,self.lat,self.lon,stop.lat,stop.lon) for stop in self.stops]

    def to_json(self):
        """

        :return:
        """
        pass
