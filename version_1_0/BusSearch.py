import bisect

class BusSearch:

    def __init__(self, stops, routes, times, id=None):
        time_tups = sorted([(i,t) for i, t in enumerate(times)],key=lambda x: x[1])
        self.times = [t for id,t in time_tups]
        self.ids = [id for id,t in time_tups]
        self.stops = stops
        self.routes = routes
        self.id = id

    def find_time_index(self, time):
        """

        :param time:
        :return:
        """
        return bisect.bisect_right(self.times, time)

    def find_stop_route(self, time):
        """

        :param time:
        :return: tuple of times, stops, routes
        """
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
        return (self.times[loc], self.stops[self.ids[loc]], self.routes[self.ids[loc]])