"""
@author Joshua E. Morgan , jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
"""
from StopBallTree import StopBallTree

class Route:
    """
    This is the route class which contains the set of stops that map
    - a route should contain all of the different stops within it
    - a route should be able to be able to be searched directionally such that it is known whether or not a given
    a given stop is down route or up route from a stop
    - a route should be able to be queried with a stop_id to get the valid transitions
    - a route should be able to display what are all the different transitions in terms of a route that can occur
    - be stored in a json format
    - be stored in a pickle format
    - be visualized using folium
    """

    def __init__(self, id, stops):
        """
        Question- double linked list, with direction
        :param stops:
        """
        # we can use a list here that is specificd in a specific direction such as
        #  inbound or outbound to insure we maintian directional selection
        self.id = id
        self.stops = {stop.id: stop for stop in stops} # build dict
        self.tree = StopBallTree(stops)
        self.order = [] # build list
        self.trans = {}

    def __str__(self):
        return (
            f"id = {self.id}"
            f"stops = {','.join(self.stops.keys())}"
        )

    def get_stop(self, stop):
        """

        :param stop:
        :return:
        """
        return self.stops[stop]

    def get_valid_exits(self, stop):
        """
        This function takes a specific stop and return
        :param stop_id:
        :return:
        """
        pass

    def get_trans(self, other_id, stop_id):
        """

        :param stop:
        :return:
        """
        return self.trans[other_id][stop_id]



    def to_json(self):
        """

        :return:
        """
        pass

    def to_pickle(self):
        """

        :return:
        """
        pass