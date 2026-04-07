import os

class BinaryTree:

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    @staticmethod
    def build_from_preorder(preorder):
        index = 0

        def helper():
            nonlocal index

            if index >= len(preorder):
                return None

            value = preorder[index]
            index += 1

            if value is None:
                return None

            node = BinaryTree(value)

            node.left = helper()
            node.right = helper()

            return node

        return helper()

    def height(self):

        def h(node):
            if node is None:
                return 0
            return 1 + max(h(node.left), h(node.right))

        return h(self)

    def _build_canvas(self):
        height = self.height()

        half = (1 << (height - 1)) - 1
        num_rows = 2 * half + 1
        num_cols = 2 * height - 1

        CW = 5

        node_grid = [[""] * num_cols for _ in range(num_rows)]
        connections = []

        root_row = half
        root_col = height - 1

        node_grid[root_row][root_col] = str(self.value)

        def place_left(node, col, center_row, pr, pc):
            if node is None:
                return

            node_grid[center_row][col] = str(node.value)
            connections.append((pr, pc, center_row, col))

            if col == 0:
                return

            gap = 1 << (col - 1)

            place_left(node.left, col - 1, center_row - gap, center_row, col)
            place_left(node.right, col - 1, center_row + gap, center_row, col)

        def place_right(node, col, center_row, pr, pc):
            if node is None:
                return

            node_grid[center_row][col] = str(node.value)
            connections.append((pr, pc, center_row, col))

            if col == num_cols - 1:
                return

            gap = 1 << (num_cols - col - 2)

            place_right(node.left, col + 1, center_row - gap, center_row, col)
            place_right(node.right, col + 1, center_row + gap, center_row, col)

        if self.left:
            place_left(self.left, root_col - 1, root_row, root_row, root_col)

        if self.right:
            place_right(self.right, root_col + 1, root_row, root_row, root_col)

        W = num_cols * CW
        num_canvas_rows = num_rows * 2 - 1

        canvas = [[" "] * W for _ in range(num_canvas_rows)]

        def cx(col):
            return col * CW + CW // 2

        def canvas_row(r):
            return r * 2

        for r in range(num_rows):
            for c in range(num_cols):

                val = node_grid[r][c]

                if val:
                    cr = canvas_row(r)
                    x = cx(c) - len(val) // 2

                    for i, ch in enumerate(val):
                        if 0 <= x + i < W:
                            canvas[cr][x + i] = ch

        for (pr, pc, cr, cc) in connections:
            px = cx(pc)
            chx = cx(cc)

            val_p = node_grid[pr][pc]
            val_c = node_grid[cr][cc]

            half_p = len(val_p) // 2 + 1
            half_c = len(val_c) // 2 + 1

            p_canvas = canvas_row(pr)
            c_canvas = canvas_row(cr)

            if pr == cr:
                row = p_canvas

                if px < chx:
                    x0, x1 = px + half_p, chx - half_c
                else:
                    x0, x1 = chx + half_c, px - half_p

                for x in range(x0, x1 + 1):
                    if 0 <= x < W:
                        canvas[row][x] = "-"

            else:
                child_above = (cr < pr)
                child_left = (cc < pc)

                conn_row = (p_canvas + c_canvas) // 2

                if child_left:
                    diag = "\\" if child_above else "/"
                    diag_x = chx + half_c

                    x0, x1 = px + half_p, diag_x - 1

                else:
                    diag = "/" if child_above else "\\"
                    diag_x = chx - half_c

                    x0, x1 = diag_x + 1, px - half_p

                if 0 <= conn_row < num_canvas_rows and 0 <= diag_x < W:
                    canvas[conn_row][diag_x] = diag

                for x in range(x0, x1 + 1):
                    if 0 <= x < W and canvas[p_canvas][x] == " ":
                        canvas[p_canvas][x] = "-"

        lines = []

        for row in canvas:
            line = "".join(row).rstrip()
            if line.strip():
                lines.append(line)

        return "\n".join(lines)

    def __str__(self):
        return self._build_canvas()
    
    def __repr__(self):
        return f"BinaryTree({self.value})"


def read_preorder(filename):
    if not os.path.exists(filename):
        print("Файл не знайдено")
        return None

    with open(filename) as f:
        data = f.read().split()

    preorder = []

    for v in data:
        if v.lower() == "none":
            preorder.append(None)
        else:
            preorder.append(v)

    return preorder

if __name__ == "__main__":
    filename = "tree.txt"
    pre = read_preorder(filename)

    tree = BinaryTree.build_from_preorder(pre)

    print(f"Дерево з файлу {filename}")
    print("=" * 100)

    print(tree)