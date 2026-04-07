import unittest
from avl_priority_queue import AVLPriorityQueue


class TestAVLPriorityQueue(unittest.TestCase):

    def setUp(self):
        self.pq = AVLPriorityQueue()

    def test_insert_single(self):
        self.pq.insert("task", 5)
        self.assertEqual(self.pq.peek(), ("task", 5))

    def test_insert_multiple_priorities(self):
        self.pq.insert("a", 1)
        self.pq.insert("b", 10)
        self.pq.insert("c", 5)

        self.assertEqual(self.pq.peek(), ("b", 10))

    def test_insert_equal_priorities(self):
        self.pq.insert("a", 5)
        self.pq.insert("b", 5)

        top = self.pq.peek()
        self.assertIn(top[0], ["a", "b"])
        self.assertEqual(top[1], 5)

    def test_extract_max(self):
        self.pq.insert("a", 1)
        self.pq.insert("b", 10)
        self.pq.insert("c", 5)

        value, priority = self.pq.extract_max()

        self.assertEqual(value, "b")
        self.assertEqual(priority, 10)

    def test_extract_order(self):
        self.pq.insert("a", 3)
        self.pq.insert("b", 7)
        self.pq.insert("c", 1)

        res = [
            self.pq.extract_max(),
            self.pq.extract_max(),
            self.pq.extract_max()
        ]

        self.assertEqual(res, [
            ("b", 7),
            ("a", 3),
            ("c", 1)
        ])

    def test_extract_empty(self):
        self.assertIsNone(self.pq.extract_max())

    def test_peek_does_not_remove(self):
        self.pq.insert("a", 10)
        self.pq.insert("b", 5)

        first = self.pq.peek()
        second = self.pq.peek()

        self.assertEqual(first, second)

    def test_peek_empty(self):
        self.assertIsNone(self.pq.peek())

    def test_many_insertions(self):
        for i in range(100):
            self.pq.insert(f"task{i}", i)

        value, priority = self.pq.peek()

        self.assertEqual(priority, 99)

    def test_mixed_operations(self):
        self.pq.insert("a", 4)
        self.pq.insert("b", 8)
        self.pq.insert("c", 2)

        self.pq.extract_max()
        self.pq.insert("d", 10)

        self.assertEqual(self.pq.peek(), ("d", 10))


if __name__ == "__main__":
    unittest.main()
