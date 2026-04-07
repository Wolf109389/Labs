import unittest
from BinaryTree import BinaryTree, find_successor


class TestFindSuccessor(unittest.TestCase):

    def setUp(self):
        """
              10
             /  \
            5    15
           / \     \
          3   7     20
              	   /
                  12
        """

        self.root = BinaryTree(10)

        self.root.left = BinaryTree(5, parent=self.root)
        self.root.right = BinaryTree(15, parent=self.root)

        self.root.left.left = BinaryTree(3, parent=self.root.left)
        self.root.left.right = BinaryTree(7, parent=self.root.left)

        self.root.right.right = BinaryTree(20, parent=self.root.right)
        self.root.right.right.left = BinaryTree(12, parent=self.root.right.right)

    # 1 Вузол має праве піддерево
    def test_node_with_right_subtree(self):
        node = self.root.left  # 5
        successor = find_successor(self.root, node)
        self.assertEqual(successor.value, 7)

    # 2 Вузол без правого піддерева
    def test_node_without_right_subtree(self):
        node = self.root.left.right  # 7
        successor = find_successor(self.root, node)
        self.assertEqual(successor.value, 10)

    # 3 Вузол у правому піддереві
    def test_node_in_right_subtree(self):
        node = self.root.right  # 15
        successor = find_successor(self.root, node)
        self.assertEqual(successor.value, 12)

    # 4 Корінь
    def test_root_successor(self):
        node = self.root  # 10
        successor = find_successor(self.root, node)
        self.assertEqual(successor.value, 15)

    # 5 Найбільший елемент
    def test_largest_node(self):
        node = self.root.right.right  # 20
        successor = find_successor(self.root, node)
        self.assertIsNone(successor)


if __name__ == "__main__":
    unittest.main()