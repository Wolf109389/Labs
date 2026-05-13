import unittest
from src.lab import solve_ijones

class TestIJones(unittest.TestCase):
    def test_example_1(self):
        grid = ["aaa", "cab", "def"]
        self.assertEqual(solve_ijones(3, 3, grid), 5)

    def test_example_2(self):
        grid = ["abcdefaghi"]
        self.assertEqual(solve_ijones(10, 1, grid), 2)

    def test_small_grid(self):
        grid = ["a"]
        self.assertEqual(solve_ijones(1, 1, grid), 1)

if __name__ == "__main__":
    unittest.main()