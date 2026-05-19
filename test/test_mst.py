import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.mst import prim_mst, add_vertex_to_mst


class TestMST(unittest.TestCase):

    def test_prim_basic(self):
        matrix = [
            [0, 3, 0],
            [3, 0, 2],
            [0, 2, 0],
        ]

        edges, weight = prim_mst(matrix)

        self.assertEqual(weight, 5)
        self.assertEqual(len(edges), 2)

    def test_single_vertex_addition(self):
        mst = [(0, 1, 3), (1, 2, 2)]

        new_edges = [
            (3, 0, 5),
            (3, 1, 1),
            (3, 2, 4),
        ]

        updated = add_vertex_to_mst(mst, new_edges)

        self.assertIn((3, 1, 1), updated)

    def test_mst_structure(self):
        matrix = [
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0],
        ]

        edges, weight = prim_mst(matrix)

        self.assertEqual(weight, 3)


if __name__ == "__main__":
    unittest.main()