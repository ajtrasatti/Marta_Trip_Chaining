
from sklearn.neighbors import BallTree
from ball_tree_helper import BallTreeHelper

class TransBuilder:

    def __init__(self,trans_limit):
        self.trans_limit = trans_limit
        helper = BallTreeHelper()
        self.ball_trees = {}

    def build_ball_tree(self, route):
        """
        This function builds the new ball tree if the ball tree has yet to be constructed
        :param route:
        :return:
        """
        if route.id not in self.ball_trees.keys():
            self.ball_trees[route.id] = self.helper.build_ball_tree(route.stops.values())
            return self.ball_trees[route.id]
        else:
            return self.ball_trees[route.id]

    def __call__(self, route1, route2):
        tree = self.build_ball_tree(route1)

