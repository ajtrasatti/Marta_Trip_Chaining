import pandas as pd
from collections import defaultdict


class ODX:
    def __init__(self):
        self.stop_count = defaultdict(lambda: 0)

    def count(self, stop, count):
        self.stop_count[stop] += count

    def count_stop_uses(self, od_counts):
        # Find the counts for how many times each stop was used as a origin or destination
        for origin, destination, count in od_counts:
            self.count(origin, count)
            self.count(destination, count)

        stop_counts_arr = [(stop, count) for stop, count in self.stop_count.items()]
        stop_counts = pd.DataFrame(stop_counts_arr, columns=["start_stop", "count"])
        stop_counts.to_csv("Data/StopCounts_April1-10.csv", index=False)

    def count_od_uses(self, df_trips):
        groups = df_trips.groupby(["start_stop", "end_stop"])
        od_counts = [(stop[0], stop[1], len(df)) for stop, df in groups if stop[0] != -1 and stop[1] != -1]
        self.count_stop_uses(od_counts)
        print("number of od pairs", len(od_counts))
        return pd.DataFrame(od_counts, columns=["start_stop", "end_stop", "count"])


def main():
    filename = "Data/trips_April1-10.csv"
    df_trips = pd.read_csv(filename)  # , index_col=0)
    odx = ODX()

    # Get counts for each origin-destination pair
    df_odx = odx.count_od_uses(df_trips)
    df_odx.to_csv("Data/odx_April1-10.csv", index=False)


if __name__ == "__main__":
    import time
    t0 = time.time()
    main()
    print("total time", time.time() - t0)
