import bisect


class BusSearch:
    """
    BusSearch is used by the breeze loader to find what bus the person got on
    """

    def __init__(self, bus_df):  # , id=None):
        times = list(bus_df.ARRIVAL_DTM)
        stops = list(bus_df.MEGA_STOP)
        routes = list(bus_df.ROUTE_ABBR)
        time_tups = sorted([(i, t) for i, t in enumerate(times)], key=lambda x: x[1])
        self.times = [t for ind, t in time_tups]
        self.ids = [ind for ind, t in time_tups]
        self.stops = stops
        self.routes = routes
        # self.id = id

    def find_time_index(self, time):
        """

        :param time:
        :return:
        """
        return bisect.bisect_right(self.times, time)

    def find_stop_route(self, time):
        """

        :param time:
        :return: tuple of time, stop, route
        """
        # @ todo - QA need to add check that it is within a certain time window
        index = self.find_time_index(time)
        if index == 0:
            # ensures that the first time is used
            loc = index
        elif index == len(self.times):
            # ensures that the last time is used
            loc = index - 1
        else:
            if abs(time - self.times[index]) < abs(time - self.times[index-1]):
                loc = index
            else:
                loc = index - 1
        return self.times[loc], self.stops[self.ids[loc]], self.routes[self.ids[loc]]
