
from .mega_stop_fac import MegaStopFac

class RailStopFac:

    def __init__(self, limit,count =0):
        self.R = 3959.87433 * 5280  # radius of the earth in feet
        self.limit = limit
        self.count = count

    def duplicate(self,curr):
        inbound = []
        outbound = []
        for i in range(len(curr)):
            if i % 2 == 0:
                inbound.append(curr[i])
            else:
                outbound.append(curr[i])
        return inbound, outbound

    def get_rail_stops(self, train_dict):
        """

        :return:
        """
        train_routes = list(train_dict.keys())
        mega_fac = MegaStopFac(700)
        curr = train_dict[train_routes[0]]
        for r in train_routes[1:]:
            curr = mega_fac.get_train_mega_stops(curr, train_dict[r])
        else:
            for i in range(4):
                inbound, outbound = self.duplicate(curr)
                curr = mega_fac.get_train_mega_stops(inbound, outbound)
        return mega_fac.get_train_mega_stops(inbound, outbound)






