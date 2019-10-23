"""
@author Joshua E. Morgan, jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
"""
import os

class Network:
    """
    This is the network class which will store all of the data associated with the different routes.
    - look up a given route and find the set of stops
    - look up a route_id, stop_id and get the stop
    - look up a route_id, stop_id and get the valid transitions
    - be easily stored in a json format
    - be stored in a pickle format
    - The constructor should be able to be run in batch over all gtsf days
        to build a search tree to find the directory for a given day
    """

    def __init__(self,routes_dict, id, dates=None,trans_limit=10):
        """

        :param routes: dict, containing route_name to route object
        :param id: int, unique identifier for a given route
        :param dates: tup, (dt.datetime, dt.datetime, weekend) used to determine which days are valid
        """
        # new function to build route_object
        self.routes = routes_dict
        self.id = id
        self.dates = dates



    def find_stop(self,route_id,stop_id):
        """
        This function finds a given stop given its identifiers
        :param route_id:
        :param stop_id:
        :return:
        """
        return self.routes[route_id].stops[stop_id]

    def get_transition(self,route_id,stop_id):
        """
        look up a route_id, stop_id and get the valid transitions
        :param route_id:
        :param stop_id:
        :return:
        """
        if stop_id in self.routes[route_id].trans:
            return self.routes[route_id].trans[stop_id]
        else:
            return []

    def export_transition(self, path):
        """
        This is a test functi
        :param path:
        :return:
        """
        cur = os.path.abspath(os.getcwd())
        test = os.path.abspath(os.path.join(cur,'Test'))
        with open(os.path.join(test,path),'w') as fout:
            import csv
            writer = csv.writer(fout)
            writer.writerow(['ROUTE','STOP_ID','TRANS_STOPS'])
            for id, r in self.routes.items():
                for s,o in r.trans.items():
                    writer.writerow([id,str(s),[str(x) for x in o]])


    def to_json(self,path_out):
        """
        be easily stored in a json format
        :param path_out:
        :return:
        """
        pass

    def to_pickle(self,path_out):
        pass


