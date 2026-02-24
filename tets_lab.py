import unittest
from zig_zag_way import zig_zag_way
from extra_task import zig_zag_robot_way



class TestZigzag(unittest.TestCase):

    def test_5x5(self):
        matrix = [
            [1, 2, 3, 4, 5 ],
            [6, 7, 8, 9, 10],
            [11,12,13,14,15],
            [16,17,18,19,20],
            [21,22,23,24,25]
        ]
        result = zig_zag_way(matrix)
        self.assertEqual(result, [1,2,6,11,7,3,4,8,12,16,21,17,13,9,5,10,14,18,22,23,19,15,20,24,25])

    def test_3x3(self):
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertEqual(zig_zag_way(matrix), [1,2,4,7,5,3,6,8,9])

    def test_2x4(self):
        matrix = [
            [1,2,3,4],
            [5,6,7,8]
        ]
        self.assertEqual(zig_zag_way(matrix), [1,2,5,6,3,4,7,8])

    def test_n1(self):
        matrix = [
            [1],
            [2],
            [3]
        ]
        self.assertEqual(zig_zag_way(matrix), [1,2,3])

    def test_m6_n1(self):
        matrix = [[1],[2],[3],[4],[5],[6]]
        self.assertEqual(zig_zag_way(matrix), [1,2,3,4,5,6])

    def test_1x1(self):
        matrix = [[42]]
        self.assertEqual(zig_zag_way(matrix), [42])

    # Robot way tests
    def test_3x4(self):
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12]
        ]
        self.assertEqual(zig_zag_robot_way(matrix, weight=60), [0, 2])

    def test_3x4_exact_weight(self):
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12]
        ]
        self.assertEqual(zig_zag_robot_way(matrix, weight=50), [1, 1])

    def test_3x4_insufficient_weight(self):
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12]
        ]
        self.assertEqual(zig_zag_robot_way(matrix, weight=10), [0, 0])


if __name__ == "__main__":
    unittest.main()
