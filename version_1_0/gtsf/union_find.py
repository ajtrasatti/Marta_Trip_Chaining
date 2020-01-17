"""
@author Joshua E. Morgan, jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
"""

class UnionFind:
    """
    This class implements the UnionFind algorithm

    - attributes:
        - ids - list containing representative of a given object
        - size - the size of the overall graph
        - sz - the sz of each set
    """
    def __init__(self, matches):
        """
        This coresponds to the make_set operation
        :param matches: list, of stops
        """
        self.ids = [i for i in range(0,len(matches))]
        self.size = len(matches)
        self.sz = [1 for x in range(0,len(matches))]

    def find(self, i):
        """
        This implements the find algorithm with path compreshion
        :param i: stop to find
        :return: the representative of a given stop
        """
        root = i
        while root != self.ids[root]:
            root = self.ids[root]
        while i != root:
            next = self.ids[i]
            self.ids[i] = root
            i = next
        return root

    def union(self,i, j):
        """
        This is the union function which merges to trees.
        :param i: int, for a stop
        :param j: int, for a stop
        :return: None
        """
        root1 = self.find(i)
        root2 = self.find(j)

        if root1 == root2:
            return
        if self.sz[root1] < self.sz[root2]:
            self.sz[root2] += self.sz[root1]
            self.ids[root1] = root2
        else:
            self.sz[root1] += self.sz[root2]
            self.ids[root2] = root1


