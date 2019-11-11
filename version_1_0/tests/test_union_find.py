import unittest
from union_find import UnionFind

class TestUnionFind(unittest.TestCase):

    def test_union(self):
        uf = UnionFind([i for i in range(0,10)])
        unions = [0,2,3,3,5,5,5,5,5,5]
        for i,j in enumerate(unions):
            uf.union(i,j)

        self.assertEqual(uf.ids, [0,1,1,1,4,4,4,4,4,4], msg='Union Find merge incorrect')
        self.assertEqual(uf.find(2), 1,msg='Union find incorrect finds the representative class')



if __name__ == '__main__':
    unittest.main()
