import csv

def read_matrix(file_path: str) -> list[list[int]]:
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        return [list(map(int, row)) for row in reader]

def prim_mst(matrix: list[list[int]]) -> tuple[list[tuple[int, int, int]], int]:
    n = len(matrix)
    visited = [False] * n
    min_edge = [float("inf")] * n
    parent = [-1] * n

    min_edge[0] = 0
    total_weight = 0
    edges = []

    for _ in range(n):
        u = -1

        for i in range(n):
            if not visited[i] and (u == -1 or min_edge[i] < min_edge[u]):
                u = i

        visited[u] = True
        
        if parent[u] != -1:
            total_weight += min_edge[u]
            edges.append((parent[u], u, min_edge[u]))

        for v in range(n):
            if matrix[u][v] != 0 and not visited[v]:
                if matrix[u][v] < min_edge[v]:
                    min_edge[v] = matrix[u][v]
                    parent[v] = u

    return edges, total_weight

def solve(file_path: str) -> tuple[list[tuple[int, int, int]], int]:
    matrix = read_matrix(file_path)
    return prim_mst(matrix)


def add_vertex_to_mst(
    mst_edges: list[tuple[int, int, int]],
    new_edges: list[tuple[int, int, int]],
) -> list[tuple[int, int, int]]:
    """
    Додає нову вершину до MST.
    new_edges: ребра від нової вершини до існуючих
    """

    min_edge = min(new_edges, key=lambda x: x[2])

    mst_edges.append(min_edge)

    return mst_edges