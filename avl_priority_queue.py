class Node:
    def __init__(self, value, priority):
        self.height = 1
        self.value = value
        self.priority = priority
        self.left = None
        self.right = None


class AVLPriorityQueue:
    def __init__(self):
        self.root = None

    def balance(self, node):
        return self.height(node.left) - self.height(node.right)
    
    def height(self, node):
        return node.height if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.height(node.left),
                              self.height(node.right))

    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def insert(self, value, priority):
        self.root = self._insert(self.root, value, priority)

    def _insert(self, node, value, priority):
        if not node:
            return Node(value, priority)

        if priority > node.priority:
            node.left = self._insert(node.left, value, priority)
        else:
            node.right = self._insert(node.right, value, priority)

        self.update_height(node)
        return self._balance(node)

    def _balance(self, node):
        bf = self.balance(node)

        if bf > 1:
            if self.balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        elif bf < -1:
            if self.balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node
    
    def peek(self):
        node = self.root
        if not node:
            return None

        while node.left:
            node = node.left

        return node.value, node.priority

    def extract_max(self):
        if not self.root:
            return None

        self.root, node = self._extract_max(self.root)
        return node.value, node.priority

    def _extract_max(self, node):
        if not node.left:
            return node.right, node

        node.left, res = self._extract_max(node.left)
        self.update_height(node)
        return self._balance(node), res

    def inorder(self):
        self._inorder(self.root)

    def _inorder(self, node):
        if not node:
            return
        self._inorder(node.left)
        print(f"value={node.value}, priority={node.priority}")
        self._inorder(node.right)

