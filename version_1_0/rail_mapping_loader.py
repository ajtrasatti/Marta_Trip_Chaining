"""
@author Anthony J. Trasatti , atrasatti3@gatech.edu
@author Joshua E. Morgan , jmorgan63@gatech.edu
Socially Aware Mobility (SAM) Lab, Georgia Tech
v_1.0
"""
import pandas as pd

class RailMappingLoader:
    """

    """
    def load_rail_mappings(self, path):
        """

        :return:
        """
        rail_mappings = pd.read_csv(path)
        return rail_mappings


    def clean_rail_mappings(self, rail_mappings):
        """

        :param rail_mappings:
        :return:
        """
        rail_mappings.update(rail_mappings.stop_name.apply(lambda x: x[:len(x) - 7].strip()))  # remove STATION
        rail_mappings.drop_duplicates(subset=['stop_name'], inplace=True)
        return rail_mappings

    def fit_2_network(self, rail_mappings, routes_dict):
        """
        This function adds the mega_stop column for the rail mappings

        :param rail_mappings:
        :param routes_dict:
        :return:
        """
        x = []
        for row in rail_mappings.itertuples():
            route = routes_dict[row.route]
            stop = route.tree.query_point(row.stop_lat, row.stop_lon)
            x.append(stop.stop_id)
        rail_mappings["stop_id"] = x

        # print(rail_mappings.head())
        return rail_mappings

