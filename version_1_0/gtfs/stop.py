"""
@author Anthony J. Trasatti , atrasatti3@gatech.edu
@author Joshua E. Morgan , jmorgan63@gatech.edu
Socially Aware Mobility (SAM) Lab, Georgia Tech
v_1.0
"""

from collections import defaultdict

class Stop:
    """
    class represents a stop (ex. bus/train) in the gtfs data

    Attributes
    - stop_id - int, unique identifier for a stop
    - lat - lattitude value for a given stop
    - lon - longitude value for a given stop 
    - tran - dict {route_id : [stop_id]} contains routes pointed to Stops that are valid transitions
    - routes - array of routes that the stop belongs to
    """
    def __init__(self, stop_id, lat, lon, routes = None):
        self.stop_id = stop_id
        self.lat = lat
        self.lon = lon

        if routes is None: 
            self.routes = set()
        else:
            self.routes = set(routes)

        # self.tran = defaultdict(lambda: {}) 

    def __eq__(self, other):
        return self.stop_id == other.stop_id

    def __ge__(self, other):
        return self.stop_id >= other.stop_id

    def __lt__(self,other):
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

    # def add_tran(self, route_id, stop_id):
    #     self.tran[route_id].add(stop_id)
    # 
    # def get_tran(self, route_id):
    #     """
    #     This returns an array of stop_ids that are a valid transition (walking distance) from this stop on the given route
    #     :param route_id: route id of the route you want to check transitions from this stop
    #     :return: [stop_ids] that are a valid 
    #     """
    #     return self.tran[route_id]

    def to_tuple(self):
        return (self.stop_id, self.lat, self.lon)

    def get_lat_lon(self):
        return (self.lat,self.lon)


def test():
    s1 = Stop(30, 54, 32)
    s2 = Stop(30, 84, 82)
    s1==s2
    [print(s) for s in {s1,s2}]

if __name__ == '__main__':
    test()
